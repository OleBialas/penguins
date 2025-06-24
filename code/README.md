# Code and helper content for metadata handling

This directory contains a Python script and helper files to transform penguin dataset tables and additional metadata into the [`flat-data`](https://concepts.inm7.de/s/flat-data/unreleased/) schema for ingestion into annotation tools.


# Usage

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
                        Main namespace URL to be used for PIDs; defaults to 'https://datalad.org/ns/datamgt/'
  --output OUTPUT       Output file name, e.g. 'output.json'; prints output to 'stdout' by default
  --post                In addition to data conversion, also POST data to the backend; a base URL should be provided
  --url URL             Base URL for the backend
  --summary             Print a summary of the transformed metadata
```

Note that an existing [`dumpthings` backend setup](https://github.com/christian-monch/dump-things-server) is required for the `--post` option to function as intended, i.e. to POST all converted metadata to the backend API. In addition, the `--url` argument will need to be supplied (e.g. `https://metadata.edu.datalad.org/datamgt/record`) and also a token if required. The token should be supplied via a `.env` file that is created in the `code` directory. The content will be as follows:

```
X_DUMPTHINGS_TOKEN=<insert-token-here>
```