# Code and helper content for metadata handling

This directory contains a Python script and helper files to transform penguin dataset tables and additional metadata into the [`demo-empirical-data`](https://github.com/psychoinformatics-de/datalad-concepts/blob/main/src/demo-empirical-data/unreleased.yaml) schema for ingestion into annotation tools.


## Usage

Create a virtual environment with a recent version of Python.

Then install requirements:

```
>> pip instal -r code/requirements.txt
```

Then run the script:

```
>> python code/convert_penguins.py
```

There are several command options. To view them you can run the help command:

```
>> python code/convert_penguins.py --help

usage: convert_penguins.py [-h] [--namespace NAMESPACE] [--output OUTPUT] [--post] [--url URL] [--summary]

options:
  -h, --help            show this help message and exit
  --namespace NAMESPACE
                        Main namespace URL to be used for PIDs; defaults to 'https://example.org/ns/demo/penguins/'
  --output OUTPUT       Output file name, e.g. 'output.json'; prints output to 'stdout' by default
  --post                In addition to data conversion, also POST data to the backend; a base URL should be provided
  --url URL             Base URL for the backend
  --summary             Print a summary of the transformed metadata
```

## Usage with `dumpthings`

An existing [`dumpthings` backend setup](https://github.com/christian-monch/dump-things-server) is required for the `--post` option to function as intended, i.e. to POST all converted metadata to the backend API.

In addition, the `--url` argument will need to be supplied (e.g. `https://penguins.edu.datalad.org/api/datamgt/`) and also a token if required. The token should be supplied via a `.env` file that is created in the `code` directory. The content should be as follows:

```
X_DUMPTHINGS_TOKEN=<insert-token-here>
```

It may be that you prefer to delete existing data on the server before generating and POSTing metadata with the `convert_penguins.py` script. In that case, it is recommended to:
1. `ssh` into the server and ensure you have the required permissions / user account
2. navigate to the backend data location
3. delete the relevant backend data
4. run the `convert_penguins.py` script
5. restart the `dumpthings` service

Some example commands:

```bash
ssh edu.datalad.org
sudo -su <the-user-running-the-service>

cd <my-backend-data-directory>
rm .sqlite-records.db

python convert_penguins.py --post --url 'https://penguins.edu.datalad.org/api/datamgt/record'

systemctl --user restart dumpthings
```