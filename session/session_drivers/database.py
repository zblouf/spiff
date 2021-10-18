# -*- coding: utf_8 -*-

from spiff import db
import pickle, base64

class SessionDb:
    def __init__(self, params):
        self.params = params
        self.db = db.dbms_factory(params)

    def load(self, session, sid):
        query = 'select * from Session where session_id="'+str(sid)+'"'
        sessions = self.db.query_dict(query)
        if len(sessions)==0:
            self.loaded = False
        else:
            _session_dict = sessions[0]
            session.expiry = _session_dict["expiry"]
            session.creation_time = _session_dict["creation"]
            session.datastore.set_data("customer_id", _session_dict["customer_id"])
            session.last_action_time = _session_dict["last_action"]
            session.datastore.set_all_data(pickle.loads(base64.b64decode(_session_dict["session_data"])))
            self.loaded = True

    def create(self, session):
        query='insert into Session(session_id, customer_id, creation, expiry, last_action, session_data) values("'+str(session.sid)+'", '+str(42)+', '+str(session.creation_time)+', '+str(session.expiry)+', '+str(0)+', "'+str(base64.b64encode(pickle.dumps(session.datastore.get_all_data())))+'")'
        self.db.run_query_commit(query)

    def save(self, session):
        _cid = session.datastore.get_data("customer_id")
        if _cid==False:
            _cid =  0
        query = 'update Session set expiry='+str(session.expiry)+', customer_id='+str(_cid)+', last_action='+str(session.last_action_time)+', session_data="'+str(base64.b64encode(pickle.dumps(session.datastore.get_all_data())))+'" where session_id="'+str(session.sid)+'"'
        self.db.run_query_commit(query)

    def destroy(self, session):
        query = 'DELETE FROM Session WHERE session_id="'+str(session.sid)+'"'

    def create_environment(self):
        query = 'create table if not exists Session(session_id TEXT, customer_id INTEGER, creation REAL, expiry REAL, last_action REAL, session_data BLOB)'
        self.db.run_query_commit(query)

session_driver = SessionDb