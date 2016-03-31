import unittest
import sqlite3
import os


from lsst.syseng_db import get_table_names, get_column_names

class TestMetaDataQueries(unittest.TestCase):

    def setUp(self):
        self.root_dir = os.getenv("SYSENG_DB_DIR")
        self.test_db_name = os.path.join(self.root_dir, "tests", "testDb")
        self.test_db_name = os.path.join(self.test_db_name, "meta_data_sqlite.db")

        if os.path.exists(self.test_db_name):
            os.unlink(self.test_db_name)

        conn = sqlite3.connect(self.test_db_name)
        cc = conn.cursor()
        cc.execute("""CREATE TABLE ashli (name text, val float, dex int)""")
        conn.commit()
        cc.execute("""INSERT INTO ashli VALUES ('hello', 2.0, 3)""")
        conn.commit()
        cc.execute("""CREATE TABLE bob (address text, year int, hour float)""")
        conn.commit()
        cc.execute("""INSERT INTO bob VALUEs('111 main street', 1988, 33.4)""")
        conn.commit()
        cc.execute("""CREATE TABLE charlie (count int, xx float, yy float)""")
        conn.commit()
        cc.execute("""INSERT INTO charlie VALUES(4, 2.4, 3.14)""")
        conn.commit()
        conn.close()


    def tearDown(self):
        if os.path.exists(self.test_db_name):
            os.unlink(self.test_db_name)


    def test_table_names(self):
        """
        Test that get_table_names returns the right values
        """

        table_name_list = get_table_names(self.test_db_name)
        self.assertEqual(len(table_name_list), 3)
        self.assertIn('ashli', table_name_list)
        self.assertIn('bob', table_name_list)
        self.assertIn('charlie', table_name_list)



    def test_get_column_names(self):
        """
        Test that get_column_names returns the right values
        """
        ashli_columns = get_column_names(self.test_db_name, 'ashli')
        self.assertEqual(len(ashli_columns), 3)
        self.assertIn('name', ashli_columns)
        self.assertIn('val', ashli_columns)
        self.assertIn('dex', ashli_columns)

        bob_columns = get_column_names(self.test_db_name, 'bob')
        self.assertEqual(len(bob_columns), 3)
        self.assertIn('address', bob_columns)
        self.assertIn('year', bob_columns)
        self.assertIn('hour', bob_columns)

        charlie_columns = get_column_names(self.test_db_name, 'charlie')
        self.assertEqual(len(charlie_columns), 3)
        self.assertIn('count', charlie_columns)
        self.assertIn('xx', charlie_columns)
        self.assertIn('yy', charlie_columns)


if __name__ == "__main__":
    unittest.main()
