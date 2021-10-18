# -*- coding: utf_8 -*-

from spiff.db import dbms_factory

class DbManager:
    def __init__(self):
        self._current_pos = 0
        self._db_array = []

    def get_db_count(self):
        return len(self._db_array)

    def add_db(self, db):
        self._db_array.append(db)

    def remove_db(self, db):
        if db in self._db_array:
            self._db_array.remove(remove_db)
            return True

    def remove_db_by_index(self, index):
        remove_db = self._db_array[index]
        if remove_db:
            self._db_array.remove(remove_db)
        else:
            return False

    def remove_db_by_name(self, db_name):
        remove_db = self.get_db_by_name(db_name)
        if remove_db:
            self._db_array.remove(remove_db)
            return True
        else:
            return False

    def create_db(self, **params_dict):
        new_db = dbms_factory(params_dict)
        if new_db.is_init():
            self.add_db(new_db)
            return True
        else:
            return False

    def get_db(self, index):
        return self._db_array[index]

    def get_dbs(self):
        return self._db_array

    def get_db_by_name(self, db_name):
        _position = self.get_db_position(db_name)
        if _position == -1:
            return False
        else:
            self._current_pos = _position
            return self.get_db(_position)

    def get_db_position(self, db_name):
        db_found = False
        for _db in self._db_array:
            if _db.get_name()==db_name:
                db_found = True
                return self._db_array.index(_db)
        if db_found == False:
            return -1

    def get_first(self):
        self._current_pos = 0
        return self._db_array[self._current_pos]

    def get_last(self):
        self._current_pos = len(self._db_array) - 1
        return self._db_array[self._current_pos]

    def get_next(self):
        if self._current_pos < (len(self._db_array) - 1):
            self._current_pos += 1
            return self._db_array[self._current_pos]
        else:
            return False
    
    def get_prev(self):
        if self._current_pos > 0:
            self._current_pos -= 1
            return self._db_array[self._current_pos]
        else:
            return False
