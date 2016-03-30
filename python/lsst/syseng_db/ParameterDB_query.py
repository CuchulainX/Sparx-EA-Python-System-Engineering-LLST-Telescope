import sqlite3
import os

from ParameterTree import Parameter

__all__ = ["get_table_names", "get_column_names",
           "get_parameter_names", "keyword_query"]

class connection_cache(object):
    """
    This is essentially a thin wrapper around a dict of database connections.
    When users want to connect to a SQLite database, they can use the
    connect() method provided in this class and any existing connection
    to that file will be used.  If non exists, a new connection will be
    opened and stored for future use.
    """

    def __init__(self):
        self._connection_dict = {}

    def connect(self, file_name):
        """
        Return a connection to the database specified by file_name.  If one
        already exists, use that.  If not, open one, store it for future use,
        and return it.
        """
        if file_name in self._connection_dict:
            return self._connection_dict[file_name]

        conn = sqlite3.connect(file_name)
        self._connection_dict[file_name] = conn
        return conn

_global_connection_cache = connection_cache()


def _convert_row_to_parameter(row):
    """
    Convert a raw of our SQLite database into a Parameter object.
    """
    name = row[0]
    values = {'defaultValue':row[1],
               'upperValue':row[2],
               'lowerValue':row[3]}

    if str(row[4]) != 'NULL':
        units = row[4]
    else:
        units = None

    if str(row[5]) != 'NULL':
        doc = row[5]
    else:
        doc = None

    if str(row[6]) != 'NULL':
        source = row[6]
    else:
        source = None

    return Parameter(name, doc=doc, units=units, values=values, source=source)

def get_table_names(db_name):
    """
    Return as list of the names of the tables on the database specified by
    db_name.
    """

    if not os.path.exists(db_name):
        raise RuntimeError("Database %s does not exist" % db_name)

    cursor = _global_connection_cache.connect(db_name).cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    results = cursor.fetchall()
    return sorted([str(rr[0]) for rr in results], key=lambda s: s.lower())


def get_column_names(db_name, table_name):
    """
    Return a list of the names of the rows in the table specified by
    table_name in the database specified by db_name.
    """

    if not os.path.exists(db_name):
        raise RuntimeError("Database %s does not exist" % db_name)

    if ')' in table_name:
        raise RuntimeError("%s is not a valid table_name" % table_name)
    cursor = _global_connection_cache.connect(db_name).cursor()
    cursor.execute("PRAGMA table_info(%s)" % table_name)
    raw_results = cursor.fetchall()
    return [str(rr[1]) for rr in raw_results]


def get_parameter_names(db_name, table_name):
    """
    Return a list of all of the parameters contained in the table specified
    by table_name in the database specified by db_name.
    """
    if not os.path.exists(db_name):
        raise RuntimeError("Database %s does not exist" % db_name)
    if ')' in table_name:
        raise RuntimeError("%S is not a valid table_name" % table_name)

    cursor = _global_connection_cache.connect(db_name).cursor()
    cursor.execute("SELECT DISTINCT name FROM %s" % table_name)
    raw_results = cursor.fetchall()
    return sorted([str(rr[0]) for rr in raw_results], key=lambda s: s.lower())


def keyword_query(db_name, table_name, keyword_list):
    """
    Query the database db_name and table table_name for all Parameters
    whose names or docstrings contain one of the keywords specified in
    keyword_list.  Returns a list of Parameter objects.
    """

    if not os.path.exists(db_name):
        raise RuntimeError("Database %s does not exists" % db_name)

    cmd = "SELECT * from %s" % table_name
    like_statement = None
    formatted_kw_list = []
    list_of_chars = []
    for kw in keyword_list:
        list_of_chars.append("%{}%".format(kw))
        list_of_chars.append("%{}%".format(kw))
        if like_statement is None:
            like_statement = " WHERE name LIKE ? OR docstring like ?"
        else:
            like_statement += " OR name LIKE ? OR docstring like ?"

    cursor = _global_connection_cache.connect(db_name).cursor()

    cmd+=like_statement

    cursor.execute(cmd, tuple(list_of_chars))
    results = cursor.fetchall()
    output = []
    for rr in results:
        output.append(_convert_row_to_parameter(rr))
    return output
