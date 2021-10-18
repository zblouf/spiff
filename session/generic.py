# -*- coding: utf_8 -*-

import time

class Session:
    def __init__(self, req, sid = None, driver = None):
        self.datastore = SimpleDataStore()
        self.set_data('isValid', False)
        self.set_data('isAuth', False)
        self.req = req
        self.sid = sid
        import session_drivers
        if driver != None:
            if driver["type"] in dir(session_drivers):
                driver_module = getattr(session_drivers, driver["type"])
                self.driver = driver_module.session_driver(driver["params"])
            else:
                self.init = False
                return 
        if sid != None:
            self.load(sid)
        else:
            self.create()

        req.answer.set_cookie(req.config.session["cookie_name"], self.sid)
        #req.answer.set_cookie(req.config.session.cookie_name, self.sid)
            #self.sid = ''
        #self.creation_time = time.time()
        #self.firstlog_time = 0
        #self.lastaction_time = 0
        #self.expiry = 0
        #self.datastore = SimpleDataStore()

    def is_valid(self):
        return self.valid

    def is_auth(self):
        return self.auth

    def create(self):
        from spiff.session import utils
        self.sid = utils.create_id()
        self.creation_time = time.time()
        self.first_login_time = 0
        self.last_action_time = 0
        self.expiry = self.creation_time + self.req.config.session["default_lifetime"]
        #self.expiry = self.creation_time + self.req.config.session.default_lifetime
        self.auth = False
        self.valid = True

        #self.datastore.set_data("customer_id", 42)
        self.datastore.set_data("isAdmin", False)
        self.datastore.set_data("isAuth", False)

        _cookie_name = self.req.config.session["cookie_name"]
        #_cookie_name = self.req.config.session.cookie_name
        self.req.answer.set_cookie(_cookie_name, self.sid)
        self.driver.create(self)
        #self.save()

    def load(self, sid = None):
        self.sid = sid
        _cookie_name = self.req.config.session["cookie_name"]
        #_cookie_name = self.req.config.session.cookie_name
        self.driver.load(self, sid)
        if not self.driver.loaded:
            self.create()
        else:
            self.req.answer.set_cookie(_cookie_name, self.sid)
            #if self.expiry > time.time():
            if self.is_expired:
                self.valid = True
                if self.expiry_soon():
                    self.renew(self.req.config.session['default_lifetime']/4)
                    #self.renew(self.req.config.session.default_lifetime/4)
            else:
                self.valid = False
        #self.valid = True

    def is_expired(self):
        timeleft = self.expiry - time.time()
        return timeleft<=0

    def expiry_in(self):
        return self.expiry-time.time()

    def expiry_soon(self):
        timeleft = self.expiry - time.time()
        return timeleft<=(self.req.config.session['default_lifetime']/4)
        #return timeleft<=(self.req.config.session.default_lifetime/4)

    def renew(self, delay):
        self.expiry += delay

    def save(self):
        self.driver.save(self)

    def destroy(self):
        self.datastore.cleanup()
        self.driver.destroy(self)

    # 
    # DATASTORE WRAPPERS
    # 
    def get_data(self, key):
        if self.datastore.has_key(key):
            return self.datastore.get_data(key)
        else:
            return False

    def set_data(self, key, value):
        self.datastore.set_data(key, value)

    def delete_data(self, key):
        self.datastore.delete_data(key)

    def get_data_store(self):
        return self.datastore

class SimpleDataStore:
    def __init__(self):
        self.data = {}

    def cleanup(self):
        self.data = {}

    def has_key(self, key):
        return self.data.has_key(key)

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        if self.data.has_key(key):
            return self.data[key]
        else:
            return False

    def get_all_data(self):
        return self.data

    def set_all_data(self, data_dict):
        self.data = data_dict

    def delete_data(self, key):
        if self.data.has_key(key):
            del self.data[key]
