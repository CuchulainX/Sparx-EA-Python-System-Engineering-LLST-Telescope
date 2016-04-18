import unittest
import os
import copy

from lsst.syseng_db import db_from_param_list, name_query, ParameterTree
from lsst.syseng_db import syseng_db_config

class TestNamequeries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root_dir = os.getenv("SYSENG_DB_DIR")
        cls.source_1 = "Telescope Requirements_v1.xml"
        cls.source_2 = "OSS_Detail_OpticalSystem_v1.xml"
        cls.data_file_1 = os.path.join(cls.root_dir, "data", "v_0_0", cls.source_1)
        cls.data_file_2 = os.path.join(cls.root_dir, "data", "v_0_0", cls.source_2)
        syseng_db_config["db_dir"] = os.path.join(cls.root_dir, "tests", "testDb")
        syseng_db_config["db_name"] = "name_query_test_db_sqlite.db"
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


    def test_name_query(self):
        """
        Test that when you query parameters by name, you get all instances of those parameters.
        Do this by querying for the name of a parameter we know exists in two xml files.
        """

        results = name_query(self.full_db_name, self.test_table, ["m1_6thAsphere"])
        self.assertEqual(len(results), 2)
        list_of_xml = [results[0].source, results[1].source]
        self.assertIn("Telescope Requirements_v1.xml", list_of_xml)
        self.assertIn("OSS_Detail_OpticalSystem_v1.xml", list_of_xml)


    def test_many_name_query(self):
        """
        Test that, when you ask for several parameter names, you get all of the instances of each.
        Do this by querying on the name of two parameters that exist in two xml files, and one that
        exists only in one.
        """

        results = name_query(self.full_db_name, self.test_table, ["m1_6thAsphere",
                                                                 "m1ConicConstant",
                                                                 "10min_track_goal"])

        self.assertEqual(len(results), 5)
        xml_dict = {}
        for rr in results:
            if rr.name not in xml_dict:
                xml_dict[rr.name] = [rr.source]
            else:
                xml_dict[rr.name].append(rr.source)

        self.assertIn("Telescope Requirements_v1.xml", xml_dict["m1_6thAsphere"])
        self.assertIn("OSS_Detail_OpticalSystem_v1.xml", xml_dict["m1_6thAsphere"])
        self.assertIn("Telescope Requirements_v1.xml", xml_dict["m1ConicConstant"])
        self.assertIn("OSS_Detail_OpticalSystem_v1.xml", xml_dict["m1ConicConstant"])
        self.assertIn("Telescope Requirements_v1.xml", xml_dict["10min_track_goal"])


if __name__ == "__main__":
    unittest.main()
