# Penguin dataset metadata curation / transformation to flat-data schema

from argparse import ArgumentParser
from dotenv import load_dotenv
from pathlib import Path
import csv
import json
import os
import requests
import sys

data = {} # Main dictionary to store annotated metadata
repo_path = Path(__file__).resolve().parent.parent
csv_files = {
    'adelie': repo_path / 'adelie' / 'table_219.csv',
    'gentoo': repo_path / 'gentoo' / 'table_220.csv',
    'chinstrap': repo_path / 'chinstrap' / 'table_221.csv',
}
meta_file = repo_path / 'code' / 'meta.json'
column_file = repo_path / 'code' / 'columns.json'
main_ns = 'https://datalad.org/ns/datamgt/'
nampespace_suffix = {
    'Dataset': 'ds',
    'DataItem': 'di',
    'Dimension': 'dim',
    'Factor': 'fact',
    'Instrument': 'inst',
    'Organization': 'org',
    'Person': 'person',
    'Protocol': 'prot',
    'Study': 'study',
    'StudyActivity': 'sact',
    'Subject': 'subj',
    'SubjectType': 'stype',
    'Unit': 'unit',
}
dump_base_url = ''


def read_csv_file(file_path):
    """
    Load content from a CSV file into an iterable of python dicts
    """
    try:
        with open(file_path, newline='') as csvfile:
            content = csv.DictReader(csvfile)
            new_content = []
            for row in content:
                new_content.append(row)
            return new_content
    except OSError as err:
        print('OS error: {0}'.format(err))
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise


def read_json_file(file_path):
    """
    Load content from a json file into a python dict
    """
    try:
        with open(file_path) as f:
            return json.load(f)
    except OSError as err:
        print('OS error: {0}'.format(err))
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise


def get_pid(class_name, pid_key):
    """
    Use base url, class-specific suffix, and unique key to construct a pid
    """
    return f'{main_ns}{nampespace_suffix[class_name]}/{pid_key}'


def add_nodes(source_meta, class_name, relationships = {}, ignore_keys = []):
    """
    Add all nodes, i.e. all records, of a specific type from the helper metadata
    to the output data dict
    """
    for key in source_meta[class_name]:
        if key in ignore_keys:
            continue
        val = source_meta[class_name][key]
        obj = val.copy()
        obj['pid'] = get_pid(class_name, key)
        for r in relationships:
            obj[r] = relationships[r]
        add_node(class_name, obj['pid'], obj)


def add_node(class_name, pid, val = {}):
    """
    Add a node, i.e. a specific record of a specific type, to the output data dict
    """
    if class_name not in data:
        data[class_name] = {}
    if pid not in data[class_name]:
        data[class_name][pid] = val
    # else:
    #     print(f'WARNING: Node already exists in data: {[pid]}')

def get_subject_dict(row, study_pid):
    """
    Create the standard structure for a 'Subject' record
    """
    stype, stype_pid = get_subject_type(row)
    sname = get_subject_id(row)
    spid = get_pid('Subject', f'{stype}_{sname}')

    stype_dict = get_data_record('SubjectType', 'pid', stype_pid)

    return {
        'study': study_pid,
        'name': sname,
        'subject_type': stype_pid,
        # 'derived_from': '',
        # 'description': '',
        'display_label': f'Penguin {sname} ({stype_dict['short_name']})',
        'pid': spid
    }

def get_subject_id(row):
    """
    Get the ID of a 'Subject' record from the associated column in table data
    """
    return row['Individual ID']


def get_subject_type(row):
    """
    Get the type of 'Subject' from the 'Species' column in table data
    """
    stype_string = row['Species']
    st = 'SubjectType'
    pidkeys = ['adelie', 'gentoo', 'chinstrap']

    for key in pidkeys:
        if key in stype_string.lower():
            return key, get_pid(st, key)
        
    raise f'subject type not known: {row}'


def get_data_record(class_name, key, val):
    """
    Get a specific record from the output data dict, given a class, key and value
    """
    return next((item for item in data[class_name].values() if item[key] == val), None)


def get_study_activity_dict(row, source_key, source_dict, study_pid, subject_pid):
    """
    Create the standard structure for a 'StudyActivity' record
    """
    anvers_pid = get_pid('Factor', 'anvers')
    factor_pid = None
    island_string = row['Island'].lower()
    for fpid in data['Factor']:
        fkey = fpid.split('/')[-1]
        if fkey in island_string:
            factor_pid = get_pid('Factor', fkey)

    return {
        'study': study_pid,
        'subjects': [subject_pid],
        'implements': [get_pid('Protocol', prot ) for prot in source_dict['implements']],
        'factors': [anvers_pid, factor_pid] if factor_pid else [anvers_pid],
        'instruments': [get_pid('Instrument', inst ) for inst in source_dict['instruments']],
        'part_of': get_pid('StudyActivity', row['studyName']),
        'description': source_dict['description'],
        'display_label': source_key,
        'pid': get_pid('StudyActivity', source_key),
    }

def get_data_item_dict(row, cname, ds_pid, sa_pid, subject_pid, dim_pid, unit_pid):
    """
    Create the standard structure for a 'DataItem' record
    """
    dim_key = dim_pid.split('/')[-1]
    sub_key = subject_pid.split('/')[-1]
    name = f'{dim_key}_of_{sub_key}_during_{row['studyName']}'

    di = {
        'part_of': ds_pid,
        'generated_by': sa_pid,
        'derived_from': subject_pid, 
        'value': row[cname],
        'dimensions': [dim_pid],
        'description': name.replace('_', ' '),
        'display_label': name,
        'pid': get_pid('DataItem', name),
    }

    if unit_pid:
        di['unit'] = unit_pid

    return di



def post_record(endpoint_class: str, token: str, record: dict):
    """
    Make a POST request to a constructred URL with a JSON body.
    From: https://hub.psychoinformatics.de/inm7/curation-utils/src/branch/main/src/inm7meta/post_data.py
    """
    headers = {
        'X-DumpThings-Token': token,
        'Content-Type': 'application/json',
    }

    # Convert the data dictionary to a JSON string
    json_data = json.dumps(record)

    try:
        response = requests.post(
            f'{dump_base_url}/{endpoint_class}',
            headers=headers,
            data=json_data,
        )
        # Check if the request was successful
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        # Return the response JSON if the response is in JSON format
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        raise


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument(
        "--namespace",
        type=str,
        help="Main namespace URL to be used for PIDs; defaults to 'https://datalad.org/ns/datamgt/'"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="stdout",
        help="Output file name, e.g. 'output.json'; prints output to 'stdout' by default"
    )
    parser.add_argument(
        "--post",
        action='store_true',
        help="In addition to data conversion, also POST data to the backend; a base URL should be provided",
    )
    parser.add_argument(
        "--url",
        type=str,
        help="Base URL for the backend",
    )
    parser.add_argument(
        "--summary",
        action='store_true',
        help="Print a summary of the transformed metadata",
    )
    args = parser.parse_args()

    output = args.output
    post = args.post
    url = args.url
    namespace = args.namespace
    summary = args.summary

    if namespace:
        main_ns = namespace

    if post and not url:
        raise ValueError(
            "The '--url' argument is required for POSTing data to the backend API"
        )
    if post and url:
        dump_base_url = url
    if output != 'stdout':
        if output.endswith('.json'):
            outfile = repo_path / 'code' / output
        else:
            outfile = repo_path / 'code' / f'{output}.json'
    
    # Load source metadata
    source_metadata = read_json_file(meta_file)
    column_descriptions = read_json_file(column_file)

    # ORGANIZATION
    # First independent organizations, ignore palmer
    palmer_org_pid = get_pid('Organization', 'palmer_station')
    add_nodes(source_metadata, 'Organization', {}, ['palmer_station'])
    # Then the dependent palmer
    org_dict = source_metadata['Organization']['palmer_station']
    ltern_org_pid = get_pid('Organization', 'ltern')
    org_dict['parent_organization'] = ltern_org_pid
    org_dict['pid'] = palmer_org_pid
    add_node('Organization', palmer_org_pid, org_dict)

    # PERSON
    # Only one
    person_key = 'kbgorman'
    person_pid = get_pid('Person', person_key)
    person_dict = source_metadata['Person'][person_key]
    person_dict['member_of'] = [get_pid('Organization', 'uni_alaska_fairbanks')]
    person_dict['pid'] = person_pid
    add_node('Person', person_pid, person_dict)

    # DATASET
    # Add the main dataset
    main_ds_pid_key = 'penguins'
    main_ds_pid = get_pid('Dataset', main_ds_pid_key)
    main_ds_val = source_metadata['Dataset'][main_ds_pid_key]
    main_ds_val['pid'] = main_ds_pid
    main_ds_val['record_contact'] = person_pid

    add_node('Dataset', main_ds_pid, main_ds_val)
    # Add child datasets and include part_of relationship
    ds_relationships = {
        'part_of': main_ds_pid,
        'record_contact': person_pid
    }
    add_nodes(source_metadata, 'Dataset', ds_relationships, [main_ds_pid_key])

    # DIMENSION
    add_nodes(source_metadata, 'Dimension')

    # FACTOR
    add_nodes(source_metadata, 'Factor')

    # INSTRUMENT
    add_nodes(source_metadata, 'Instrument')

    # PROTOCOL
    add_nodes(source_metadata, 'Protocol')

    # UNIT
    add_nodes(source_metadata, 'Unit')

    # STUDY
    study_pid = get_pid('Study', main_ds_pid_key)
    study_val = source_metadata['Study'][main_ds_pid_key]
    study_val['pid'] = study_pid
    # relational objects must exist before they can be referenced here
    study_relationships = {
        'implements': list(data['Protocol'].keys()),
        'factors': list(data['Factor'].keys()),
        'instruments': list(data['Instrument'].keys()),
        'dimensions': list(data['Dimension'].keys()),
        'record_contact': person_pid
    }
    for r in study_relationships:
        study_val[r] = study_relationships[r]
    
    add_node('Study', study_pid, study_val)

    # MAIN STUDYACTIVITYs

    for sact_key in source_metadata['StudyActivity']:
        main_sa = source_metadata['StudyActivity'][sact_key]
        main_sa['study'] = study_pid
        main_sa['pid'] = get_pid('StudyActivity', sact_key)
        add_node('StudyActivity', main_sa['pid'], main_sa)

    # SUBJECTTYPE
    add_nodes(source_metadata, 'SubjectType')

    # Next: process each `Dataset`'s CSV table
    # First setup some tracking/storage variables
    unique_subs = set()
    dimensions = data['Dimension']
    factors = data['Factor']
    units = data['Unit']
    instruments = data['Instrument']
    protocols = data['Protocol']
    source_study_activities = source_metadata['StudyActivityPerSubjectBasis']
    source_units_for_dimensions = source_metadata['DimensionToUnitMapping']
    study_activities = []
    dataset_row_counts = []
    
    # Read table per dataset
    for dataset_key in csv_files:
        dataset_pid = get_pid('Dataset', dataset_key)
        csv_content = read_csv_file(csv_files[dataset_key])
        dataset_row_counts.append(len(csv_content))
        # Iterate over rows of table
        for row in csv_content:
            # Create subject
            sub = get_subject_dict(row, study_pid)
            sub_key = sub['pid'].split('/')[-1]
            unique_subs.add(sub['pid'])
            # add subject to data if it does not yet exist there
            add_node('Subject', sub['pid'], sub)

            # for each custom studyactivity done per subject:
            for s in source_study_activities:
                sa = source_study_activities[s]
                sa_key = s.replace('<X>', sub_key).replace('<Y>', row['studyName'])
                # if all column values related to data items that are generated by this
                # activity are empty, then we continue to the next iteration, because
                # then the studyactivity does not generate any of the dataitems and it
                # should not be created
                generates_something = False
                for c in sa['_generatesDataItemWithDim']:
                    cname = source_metadata['Dimension'][c]['name']
                    if row[cname]:
                        generates_something = True
                if not generates_something:
                    continue

                # Now we create the StudyActivity
                new_sa = get_study_activity_dict(
                    row=row,
                    source_key=sa_key,
                    source_dict=sa,
                    study_pid=study_pid,
                    subject_pid=sub['pid']
                )
                add_node('StudyActivity', new_sa['pid'], new_sa)

                study_activities.append(sa_key)
                # Then we create all DataItems for which there are values in the table
                for c in sa['_generatesDataItemWithDim']:
                    cname = source_metadata['Dimension'][c]['name']
                    if row[cname]:
                        # get associated dimension
                        dim_pid = get_pid('Dimension', c)
                        # get associated unit
                        unit_pid = get_pid('Dimension', source_units_for_dimensions[c]) if source_units_for_dimensions[c] else None
                        new_data_item = get_data_item_dict(
                            row=row,
                            cname = cname,
                            ds_pid=dataset_pid,
                            sa_pid=new_sa['pid'],
                            subject_pid=sub['pid'],
                            dim_pid=dim_pid,
                            unit_pid=unit_pid,
                        )
                        add_node('DataItem', new_data_item['pid'], new_data_item)


    # OUTPUT
    if output == 'stdout':
        json.dump(data, sys.stdout)
    else:
        with open(outfile, 'w') as fp:
            json.dump(data, fp, indent=4, sort_keys=True)

    # SUMMARY
    if summary:
        print('\n\nSUMMARY')
        print('\nNumber of records per class:\n')
        for clss in data:
            print(f'{clss}: {len(data[clss].keys())}')
        print(f'\nUnique penguins:\t{len(list(unique_subs))}')
        print(f'All table rows:\t\t{sum(dataset_row_counts)} {dataset_row_counts}')

    # POST
    if post:
        load_dotenv()
        X_DUMPTHINGS_TOKEN = os.getenv('X_DUMPTHINGS_TOKEN')
        # Now we post data to backend in specific order
        post_this = [
            'Organization',
            'Person',
            'Dimension',
            'Factor',
            'Instrument',
            'Protocol',
            'Unit',
            'Dataset',
            'Study',
            'SubjectType',
            'Subject',
            'StudyActivity',
            'DataItem'
        ]
        for clss in post_this:
            cnt = 0
            print(f'\n\nPosting objects of class "{clss}"')
            for record_pid in data[clss]:
                # 'short_name' is used internally, but not part of the allowed slots for 'SubjectType'
                if clss == 'SubjectType':
                    data[clss][record_pid].pop('short_name', None)
                cnt = cnt + 1
                record = data[clss][record_pid]
                print(f'{cnt} - Posting: {record_pid}', end='\r')
                # print(record)
                posted_data = post_record(endpoint_class=clss, token=X_DUMPTHINGS_TOKEN, record=record)
    

# NOTES:

# Some 'Individual ID' values occur twice (or more), with varying 'studyName's. From this I deduce:
# - individuals can be studied multiple times, each time during a different base-StudyActivity (PAL0708, PAL0809, or PAL0910)
# - the subject remains the same for all related StudyActivities
# - `StudyActity`s need another qualifier, which is the base StudyActivity
# - Where the initial proposal was to go with something like 'DeterminingTheSexOfPenguinX', now it should be 'DeterminingTheSexOfPenguinXDuringY'

# 'Individual ID' values are not unique across datasets/species (of which we have three). This means a unique individual identifier needs more than the 'Individual ID' value -> also species.

# Procedure for each row:
# - create subject:
#   - study: argument
#   - subject_type: from 'Species'
#   - name, pid, preflabel: from 'Individual ID'
# - add subject to data, if it does not already exist there
# - For each key in 'StudyActivityPerSubjectBasis':
#   - `StudyActivity` should only be created+added if the columns associated with the `Dimension`s that it shoud create actually have values.
#   - This means we should check `row[c]` for each `c` in the `_generatesDataItemWithDim` list.
#   - Here `c` is not the same as the column heading, but maps to it via the source metadata `Dimension` dict: `cname = metadata['Dimension'][c]['name']`