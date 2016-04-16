import unittest
import os
import copy

from lsst.syseng_db import db_from_param_list, keyword_query, ParameterTree
from lsst.syseng_db import get_parameter_names
from lsst.syseng_db import syseng_db_config

class TestXMLqueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root_dir = os.getenv("SYSENG_DB_DIR")
        cls.source_1 = "Telescope Requirements_v1.xml"
        cls.source_2 = "OSS_Detail_OpticalSystem_v1.xml"
        cls.data_file_1 = os.path.join(cls.root_dir, "data", "v_0_0", cls.source_1)
        cls.data_file_2 = os.path.join(cls.root_dir, "data", "v_0_0", cls.source_2)
        syseng_db_config["db_dir"] = os.path.join(cls.root_dir, "tests", "testDb")
        syseng_db_config["db_name"] = "xml_query_test_db_sqlite.db"
        cls.full_db_name = os.path.join(syseng_db_config["db_dir"], syseng_db_config["db_name"])
        if os.path.exists(cls.full_db_name):
            os.unlink(cls.full_db_name)

        cls.test_table = "test_table"
        cls.reference_tree_1 = ParameterTree(cls.data_file_1)
        param_list = copy.deepcopy(cls.reference_tree_1.parameter_list)
        cls.reference_tree_2 = ParameterTree(cls.data_file_2)
        param_list.extend(cls.reference_tree_2.parameter_list)
        db_from_param_list(param_list, cls.test_table)


    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.full_db_name):
            os.unlink(cls.full_db_name)


    def test_xml_file_query(self):
        """
        Test that when we run keyword_query, specifying a list of xml files,
        we only get results from the expected xml files
        """

        # do a query from two .xml files which we know have redundant parameters;
        # make sure we get results from both .xml files
        gross_results = keyword_query(self.full_db_name, self.test_table, ["m1"],
                                      xml_list=[self.source_1, self.source_2])

        self.assertGreater(len(gross_results), 0)
        ct_1 = 0
        ct_2 = 0
        for pp in gross_results:
            self.assertIn(pp.source, [self.source_1, self.source_2])
            if pp.source == self.source_1:
                ct_1 += 1
            else:
                ct_2 += 1

        self.assertGreater(ct_1, 0)
        self.assertGreater(ct_2, 0)

        # do the same search, specifying only one of the .xml files;
        # make sure that we only get results from one of them
        just_1_results = keyword_query(self.full_db_name, self.test_table, ["m1"],
                                       xml_list=[self.source_1])

        self.assertGreater(just_1_results, 0)
        for pp in just_1_results:
            self.assertEqual(pp.source, self.source_1)




if __name__ == "__main__":
    unittest.main()
