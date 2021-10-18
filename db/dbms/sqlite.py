# -*- coding: utf_8 -*-

from spiff.db.dbms.generic import DbGeneric
try:
    import sqlite3
except ImportError:
    #print "Sqlite3 module importation error"
    from pysqlite2 import dbapi2 as sqlite3
#from pysqlite2 import dbapi2 as sqlite3

#sqlite_datatype_map = dict(
#						"char" = "text",
#						"varchar" = "text",
#						"numeric" = "real",
#						"decimal" = "real",
#						"integer" = "integer",
#						"smallint" = "integer",
#						"float" = "real",
#						"real" = "real",
#						"double" = "real",
#						"time" = "blob",
#						"timestamp" = "blob",
#						"interval" = "blob",
#						"blob" = "blob",
#						"varblob" = "blob"
#						)

class DbSqlite(DbGeneric):
    def __init__(self):
        DbGeneric.__init__(self)

#   def commit(self):
#       self._connection.commit()

    def open(self, params_dict):
        pass

    def connect(self, params_dict):
        self._connection = sqlite3.connect(params_dict["filename"])
        return self._connection

    def get_table_count(self):
        nb_tables = 0
        query = "SELECT name FROM sqlite_master WHERE type=\"table\""
        self.run_query_with_result(query)
        for row in self._cursor:
            nb_tables += 1
        return nb_tables

    def get_table_names(self):
        table_names = []
        query = "SELECT name FROM sqlite_master WHERE type=\"table\""
        self.run_query_with_result(query)
        for row in self._cursor:
            table_names.append(row[0])
        return table_names

    def get_field_count(self, table_name):
        nb_fields = 0
        query = "SELECT * FROM " + table_name + ""
        self.run_query_with_result(query)
        for row in self._cursor.description:
            nb_fields += 1
        return nb_fields

    def get_field_names(self, table_name):
        field_names = []
        query = "SELECT * FROM " + table_name + ""
        self.run_query_with_result(query)
        for row in self._cursor.description:
            field_names.append(row[0])
        return field_names

    def create_table(self, table_name, fields_list, override=False):
        query = "CREATE TABLE "
        if override==False:
            query = query + "IF NOT EXISTS "
        query = query+str(table_name)+"("
        count = 1
        for field in fields_list:
            query = query + str(field["name"])+" "+str(field["type"])
            if count != len(fields_list):
                query = query + ", "
            count = count + 1
        query = query+");"
        print query
        #self.runQueryWithResult(query)

db = DbSqlite
