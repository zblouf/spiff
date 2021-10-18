# -*- coding: utf_8 -*-

from spiff.db.dbms.generic import DbGeneric
import MySQLdb as mysql

class DbMysql(DbGeneric):
    def __init__(self):
        DbGeneric.__init__()
#        self._connection_params = ["host", "user", "pass", "base"]

    def open(self, params_dict):
        pass

    def connect(self, params_dict):
        self._connection = MySQLdb.Connect(params["host"], params["user"], params["pass"], params["base"])
        return self._connection
        
    def get_table_count(self):
        nb_tables = 0
        query = "SHOW TABLES"
        self.run_query_with_result(query)
        for row in self._cursor:
            nb_tables += 1
        return nb_tables

    def get_table_names(self):
        table_names = []
        query = "SHOW TABLES"
        self.run_query_with_result(query)
        for row in self._cursor:
            table_names.append(row[0])
        return table_names
        
    def get_field_count(self, table_name):
        nb_fields = 0
        query = "SHOW COLUMNS FROM `" + table_name + "`"
        self.run_query_with_result(query)
        for row in self._cursor:
            nb_fields += 1
        return nb_fields
        
    def get_field_names(self, table_name):
        field_names = []
        query = "SHOW COLUMNS FROM `" + table_name + "`"
        self.run_query_with_result(query)
        for row in self._cursor:
            field_names.append(row[0])
        return field_names