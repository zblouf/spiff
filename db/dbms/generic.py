# -*- coding: utf_8 -*-

# spiff, a python-based framework
# Copyright (c) 2006-2020, Romain Gaches, <romain@ssji.net>

class DbGeneric:
    def __init__(self):
        self._type = ""
        self._name = ""
        self._open = False
        self._params = {}

    #temporary hack
    def commit(self):
        self._connection.commit()

    def open_from_xml(self, xml_file, db_name):
        xmldoc = ElementTree.parse(xml_file)
        params = extract_db(xmldoc, db_name)
        return self.open(params)

    def open(self, params_dict):
        pass

    def close(self):
        pass

    def run_query_with_result(self, sql_query, args=()):
        self._cursor = self._connection.cursor()
        self._cursor.execute(sql_query, args)
        return self._cursor

    def run_query_commit_with_result(self, sql_query, args=()):
        self._cursor = self._connection.cursor()
        self._cursor.execute(sql_query, args)
        self.commit()
        return self._cursor

    def run_query(self, sql_query, args=()):
        self._cursor = self._connection.cursor()
        self._cursor.execute(sql_query, args)
        return self._cursor

    def run_query_commit(self, sql_query, args=()):
        self._cursor = self._connection.cursor()
        self._cursor.execute(sql_query, args)
        self.commit()
        return self._cursor

    def fetch_dict(self):
        result = []
        for row in self._cursor:
            row_dict = {}
            counter = 0
            for field in self._cursor.description:
                row_dict[field[0]] = row[counter]
                counter += 1
            result.append(row_dict)
        return result

    def query_dict(self, sql_query, args=()):
        result = self.run_query_with_result(sql_query, args)
        if result:
            return self.fetch_dict()
        else:
            return False

    def table_exists(self, table_name):
        if table_name in self.get_table_names():
            return True
        else:
            return False
