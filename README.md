This repository exists to provide two products to the LSST project and user
communities.

1) The `data/` directory should contain (in sub-directories labeled by version)
the change controlled .xml files exported by Enterprise Architect describing the
current official state of the LSST System.

2) Python scripts (in `python/lsst/syseng_db/` and managed by `EUPS`) to convert
those .xml files into an sqlite database and then easily query that database.

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
