This repository exists to provide two products to the LSST project and user
communities.

1) The `data/` directory should contain (in sub-directories labeled by version)
the change controlled .xml files exported by Enterprise Architect describing the
current official state of the LSST System.

2) Python scripts (in `python/lsst/syseng_db/` and managed by `EUPS`) to convert
those .xml files into an sqlite database and then easily query that database.

Note: In order to get the .xml files, you must have Git's LFS system installed
on your machine.  See instructions here

http://developer.lsst.io/en/latest/tools/git_lfs.html

##Generating the LSST Parameter Database

This repository is designed so that the .xml files contained in `data/` will be
stored in an sqlite database `db/LSST_parameter_sqlite.db`.  To generate (or
update) this database, run the script `scripts/update_db.py`, specifying a
sub-directory of `data/`.  `update_db.py` will read in all of the .xml files in
the specified sub-directory and load their data into a table in
`db/LSST_parameter_sqlite.db` that is named after the sub-directory.  i.e.
```
python scripts/update_db.py v_0_0
```
will read through all of the .xml files in `data/v_0_0/`, and load their data
into the table `v_0_0` in `db/LSST_parameter_sqlite.db`.  If the table `v_0_0`
already exists, an exception will be raised.  If `db/LSST_parameter_sqlite.db`
does not exist, it will be created.

##Testing the web interface

In order to run the web interface locally, you must have Flask installed
somewhere python knows about it.  If you are running anaconda (or miniconda)
```
conda install flask
```
should set you up.

To test the web interface to this system, navigate into the `web_interface/`
sub-directory and run
```
python syseng_db.py
```
This will initialize a local server.  Open a web-browser and go to
`127.0.0.1:5000/`.  You will now have access to a local copy of the web-site.

##LSST Parameter Database Schema

Each row in `db/LSST_parameter_sqlite.db` corresponds to a parameter taken from
the .xml files in `data/`.  The information stored for each parameter is defined
by the `Parameter` class defined in `python/lsst/syseng_db/ParameterTree.py`.
The columns stored in `db/LSST_parameter_sqlite.db` (which correspond to the
properties of the `Parameter` class are)

- `name`

- `defaultValue`

- `upperValue`

- `lowerValue`

- `units` (defining the units of `defaultValue`, `upperValue`, and `lowerValue`)

- `docstring` which documents the meaning of the parameter

- `source` which is the name of the .xml file in which this parameter was
defined

##Querying the LSST Parameter Database

Once `db/LSST_parameter_sqlite.db` has been created, the code in
`python/lsst/syseng_db` provides utility functions to easily query the database
and its tables.

- `get_table_names()` returns the names of the tables in a database that you
specify

- `get_column_names()` returns the names of the columns in a table that you
specify

- `keyword_query` allows you to query a specific table for all `Parameters` that
contain certain keywords in either their names or their docstrings.

Note: all of these methods require you to specify the name of the database you
are querying.  The default database and its resident directory are specified in
the dict `syseng_db_config`, i.e.
```
import os
from lsst.syseng_db import syseng_db_config

db_name = os.path.join(syseng_db_config['db_dir'], syseng_db_config['db_name'])
```
will give you the absolute path to `LSST_parameter_sqlite.db`.

`keyword_query` will return its results as a list of `Parameter` objects
(`Parameter` being the class defined in `python/lsst/syseng_db/ParameterTree.py`
which carries around the data of a parameter defined in the .xml files).
`Parameter` comes with a method `write_param()` which will write the contents of
the `Parameter` in a human-friendly format, thus
```
results = keyword_query(db_name, 'v_0_0', ['velocity'])
for param in results:
    param.write_param()
```
will print all of the parameters with the word 'velocity' in either their
name or docstring to the screen.
