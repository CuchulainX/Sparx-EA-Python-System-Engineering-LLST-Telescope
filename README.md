This repository exists to provide two products to the LSST project and user
communities.

1) The `data/` directory should contain (in sub-directories labeled by version)
the change controlled .xml files exported by Enterprise Architect describing the
current official state of the LSST System.

2) Python scripts (in `python/lsst/syseng_db/` and managed by `EUPS`) to convert
those .xml files into an sqlite database and then easily query that database.

##Generating the LSST Parameter Database
