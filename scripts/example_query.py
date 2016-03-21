"""
This is an example script which queries LSST_parameter_sqlite.db for all of
the parameters with the word 'throughput' in either their name or their
docstring and writes them out to a file 'example_output.txt'
"""

from __future__ import with_statement
import os
from lsst.syseng_db import keyword_query
from lsst.syseng_db import syseng_db_config

if __name__ == "__main__":

    db_name = os.path.join(syseng_db_config['db_dir'],
                           syseng_db_config['db_name'])


    if not os.path.exists(db_name):
        raise RuntimeError("LSST_parameter_sqlite.db does not exist.\n"
                           + "Run scripts/update_db.py with command line arg\n"
                           + "'v_0_0' to create the database and populate the\n"
                           + "table 'v_0_0'.")

    with open("example_output.txt", "w") as output_file:
        results = keyword_query(db_name, 'v_0_0', ["throughput"])
        for param in results:
            param.write_param(output_file)
