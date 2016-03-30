import unittest
import os

from lsst.syseng_db import db_from_xml_file, keyword_query, ParameterTree
from lsst.syseng_db import get_parameter_names
from lsst.syseng_db import syseng_db_config

class TestDBqueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root_dir = os.getenv("SYSENG_DB_DIR")
        cls.data_file = os.path.join(cls.root_dir, "data", "v_0_0", "Science_Requirements_v1.xml")
        syseng_db_config["db_dir"] = os.path.join(cls.root_dir, "tests", "testDb")
        syseng_db_config["db_name"] = "query_test_db_sqlite.db"
        cls.full_db_name = os.path.join(syseng_db_config["db_dir"], syseng_db_config["db_name"])
        if os.path.exists(cls.full_db_name):
            os.unlink(cls.full_db_name)

        cls.test_table = "test_table"
        db_from_xml_file(cls.data_file, cls.test_table)


    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.full_db_name):
            os.unlink(cls.full_db_name)


    def setUp(self):
        # Create a ParameterTree that contains all of the data in our test database
        self.reference_tree = ParameterTree(self.data_file)


    def test_one_keyword_query(self):
        """
        Test that keyword_query returns all of the Parameters in a database
        that match the keyword
        """
        keyword = "eak"
        kw_params = keyword_query(self.full_db_name, self.test_table, [keyword])
        self.assertGreater(len(kw_params), 0)

        string_list = [] # this list will contain the name+doc of all of the matching parameters

        for param in kw_params:
            name_plus_doc = str(param.name).lower() + ' ' + str(param.doc).lower()
            self.assertIn(keyword, name_plus_doc)
            string_list.append(name_plus_doc)

        # Now loop over the reference tree and check that every Parameter that matches
        # the keyword was returned by the query, and every Parameter that does not match
        # the keyword was not returned by the query.
        ct_in = 0
        ct_not_in = 0
        for param in self.reference_tree.parameter_list:
            name_plus_doc = str(param.name).lower() + ' ' + str(param.doc).lower()
            if keyword in name_plus_doc:
                ct_in += 1
                self.assertIn(name_plus_doc, string_list)
            else:
                ct_not_in += 1
                self.assertNotIn(name_plus_doc, string_list)

        # Make sure that both keyword_query and just looping over the ParameterTree
        # agree on how many Parameters matched.  Also verify that at least some
        # Parameters did not match.
        self.assertEqual(ct_in, len(kw_params))
        self.assertGreater(ct_not_in, 0)


    def test_one_camelCase_keyword_query(self):
        """
        Test that keyword_query can handle weird cases (capitalization or camelCase)
        """
        keyword = "eAk"
        kw_params = keyword_query(self.full_db_name, self.test_table, [keyword])
        self.assertGreater(len(kw_params), 0)
        string_list = [] # this list will contain the name+doc of all of the matching parameters
        for param in kw_params:
            name_plus_doc = str(param.name).lower() + ' ' + str(param.doc).lower()
            self.assertIn(keyword.lower(), name_plus_doc)
            string_list.append(name_plus_doc)


        # Now loop over the reference tree and check that every Parameter that matches
        # the keyword was returned by the query, and every Parameter that does not match
        # the keyword was not returned by the query.
        ct_in = 0
        ct_not_in = 0
        for param in self.reference_tree.parameter_list:
            name_plus_doc = str(param.name).lower() + ' ' + str(param.doc).lower()
            if keyword.lower() in name_plus_doc:
                ct_in += 1
                self.assertIn(name_plus_doc, string_list)
            else:
                ct_not_in += 1
                self.assertNotIn(name_plus_doc, string_list)

        # Make sure that both keyword_query and just looping over the ParameterTree
        # agree on how many Parameters matched.  Also verify that at least some
        # Parameters did not match.
        self.assertEqual(ct_in, len(kw_params))
        self.assertGreater(ct_not_in, 0)


    def test_two_keyword_query(self):
        """
        Test that keyword_query can handle multiple keywords at once
        """
        keyword1 = "eak"
        keyword2 = "etch"
        kw_params = keyword_query(self.full_db_name, self.test_table, [keyword1, keyword2])
        self.assertGreater(len(kw_params), 0)

        string_list = [] # this list will contain the name+doc of all of the matching parameters

        for param in kw_params:
            name_plus_doc = str(param.name).lower() + ' ' + str(param.doc).lower()
            is_kw1 = keyword1 in name_plus_doc
            is_kw2 = keyword2 in name_plus_doc
            self.assertTrue(is_kw1 or is_kw2)
            string_list.append(name_plus_doc)

        # Now loop over the reference tree and check that every Parameter that matches
        # the keyword was returned by the query, and every Parameter that does not match
        # the keyword was not returned by the query.
        ct1_in = 0
        ct2_in = 0
        ct_in = 0
        ct_not_in = 0
        for param in self.reference_tree.parameter_list:
            name_plus_doc = str(param.name).lower() + ' ' + str(param.doc).lower()
            is_kw1 = keyword1 in name_plus_doc
            is_kw2 = keyword2 in name_plus_doc
            if is_kw1 or is_kw2:
                ct_in += 1
                if is_kw1:
                    ct1_in +=1
                if is_kw2:
                    ct2_in += 1
                self.assertIn(name_plus_doc, string_list)
            else:
                ct_not_in += 1
                self.assertNotIn(name_plus_doc, string_list)

        # Make sure that both keyword_query and just looping over the ParameterTree
        # agree on how many Parameters matched.  Also verify that at least some
        # Parameters did not match.  Finally, make sure that both keywords were matched
        # independently (i.e. that not all of the returned Parameters were matched on just
        # one of the keywords)
        self.assertGreater(ct_not_in, 0)
        self.assertLess(ct1_in, len(kw_params))
        self.assertLess(ct2_in, len(kw_params))
        self.assertGreater(ct1_in, 0)
        self.assertGreater(ct2_in, 0)
        self.assertEqual(ct_in, len(kw_params))


    def test_param_names(self):
        """
        Test that get_parameter names returns the complete list of names of the parameters
        stored in the database.
        """
        names_test = get_parameter_names(self.full_db_name, self.test_table)
        for pp in self.reference_tree.parameter_list:
            self.assertIn(pp.name, names_test)
        self.assertEqual(len(self.reference_tree.parameter_list), len(names_test))


if __name__ == "__main__":
    unittest.main()
