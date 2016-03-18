import unittest
import os
from lsst.syseng_db import ParameterTree, db_from_param_list, syseng_db_config

syseng_db_dir = None
syseng_db_name = None

class DB_generation_test(unittest.TestCase):

    def test_db(self):
        root_dir = os.getenv("SYSENG_DB_DIR")

        out_dir = os.path.join(root_dir, "tests", "testDb")
        out_name = "db_creation_test_sqlite.db"

        full_out_name = os.path.join(out_dir, out_name)
        if os.path.exists(full_out_name):
            os.unlink(full_out_name)

        data_file = os.path.join(root_dir, "tests", "testData")
        data_file = os.path.join(data_file, "Science_Requirements_v1.xml")
        tree = ParameterTree(data_file)
        syseng_db_config["db_dir"] = out_dir
        syseng_db_config["db_name"] = out_name
        db_from_param_list(tree.parameter_list, 'test_table')

        self.assertTrue(os.path.exists(full_out_name))
        if os.path.exists(full_out_name):
            os.unlink(full_out_name)

if __name__ == "__main__":
    unittest.main()
