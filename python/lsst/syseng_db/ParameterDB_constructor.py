import sqlite3
import os

from ParameterTree import Parameter

__all__ = ["db_from_param_list", "syseng_db_config"]

syseng_db_config = {
                    "db_dir":os.path.join(os.getenv("SYSENG_DB_DIR"), "db"),
                    "db_name":"LSST_parameter_sqlite.db"
                    }

def db_from_param_list(param_list, table_name):
    """
    Read in a list of Parameter objects and write them into an SQLite database
    table.  The database file name will be specified by the global dict
    syseng_db_config.  Specifically, the file name will be

    os.path.join(syseng_db_config['db_dir'], syseng_db_config['db_name'])

    The name of the table to be constructed is specified by the second
    argument to this function.
    """

    file_name = os.path.join(syseng_db_config["db_dir"],
                             syseng_db_config["db_name"])

    conn = sqlite3.connect(file_name)

    cc = conn.cursor()

    cmd = """CREATE TABLE %s (name text, defaultValue text, """ % table_name \
        + """upperValue text, lowerValue text, units text, docstring text, """ \
        + """source text)"""

    cc.execute(cmd)

    conn.commit()

    for param in param_list:
        name = param.name
        if 'defaultValue' in param.values:
           default = param.values['defaultValue']
        else:
            default = 'NULL'

        if 'upperValue' in param.values:
            upper = param.values['upperValue']
        else:
            upper = 'NULL'

        if 'lowerValue' in param.values:
            lower = param.values['lowerValue']
        else:
            lower = 'NULL'

        if param.doc is not None:
            doc = param.doc
        else:
            doc = 'NULL'

        if param.units is not None:
            units = param.units
        else:
            units = 'NULL'

        if param.source is not None:
            source = param.source
        else:
            source = 'NULL'

        cc.execute("""INSERT INTO %s VALUES(?, ?, ?, ?, ?, ?, ?)""" % table_name,
                   (name, default, upper, lower, units, doc, source))

    conn.commit()
    conn.close()
