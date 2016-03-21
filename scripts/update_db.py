"""
This script will read through the contents of $SYSENG_DB_DIR/data/ and
will read the contents of each sub-directory into a new table of
$SYSENG_DB_DIR/db/LSST_parameter_sqlite.db

Call it by specifying a sub_directory of $SYSENG_DB_DIR/data/, e.g.

    python scripts/update_db.py v_0_0

The script will find all of the .xml files in that directory, and
create a table in the database specified by syseng_db_config containing
the Parameters.  The name of the table will be the same as the name of
the sub-directory ('v_0_0' in the example above).

An exception will be raised if the table already exists (or if the user
specifies something other than a sub-directory of $SYSENG_DB_DIR/data/).
"""

import sys
import os
from lsst.syseng_db import ParameterTree
from lsst.syseng_db import db_from_param_list
from lsst.syseng_db import syseng_db_config

if __name__ == "__main__":

    arguments = sys.argv

    if len(arguments)<2:
        raise RuntimeError("This script expects a sub-directory, e.g.:\n"
                           +"\n    python scripts/update_db.py dir/to/read")

    sub_dir = arguments[1]
    data_dir = os.path.join(os.getenv("SYSENG_DB_DIR"), "data", sub_dir)
    if not os.path.exists(data_dir):
        raise RuntimeError("Directory %s does not exist" % data_dir)

    if not os.path.isdir(data_dir):
        raise RuntimeError("%s is not a directory" % data_dir)

    parameter_list = []
    list_of_files = os.listdir(data_dir)
    for file_name in list_of_files:
        if file_name.endswith(".xml"):
            local_tree = ParameterTree(os.path.join(data_dir, file_name))
            parameter_list.extend(local_tree.parameter_list)

    db_from_param_list(parameter_list, sub_dir)
