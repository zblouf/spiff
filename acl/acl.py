# -*- coding: utf_8 -*-

def isAllowed(  db,
                uid,
                module,
                target_type,
                target_id,
                action):
    """
    Returns if given _user_ is allowed to perform _action_ on _module/target_.
    """
    
    _result = False
    query = 'SELECT action FROM ACL WHERE'
    query = query + ' user_id='+str(uid)
    query = query + ' module_id='+str(module)
    query = query + ' target_type='+str(target_type)
    query = query + ' target_id='+str(target_id)
    result_list = db.queryDict(query)
    if len(result_list)>0:
        result_dict = result_list[0]
        _action = result_dict['action']
        if (action & _action) != 0:
            _result = True
    return _result

def getPermissions( db,
                    uid,
                    module,
                    target_type,
                    target_id):
    """
    Returns the permissions (integer) for given _user_ on _module/target_.
    """

    _permission = 0
    query = 'SELECT action FROM ACL WHERE'
    query = query + ' user_id='+str(uid)
    query = query + ' AND module_id='+str(module)
    query = query + ' AND target_type='+str(target_type)
    query = query + ' AND target_id='+str(target_id)
    result_list = db.queryDict(query)
    if len(result_list)>0:
        result_dict = result_list[0]
        _permission = result_dict['action']
    return _permission

def getAllowedIds(  db,
                    uid,
                    module,
                    target_type,
                    action=0):
    """
    """
    _ids = []
    query = 'SELECT * FROM ACL WHERE'
    query = query + ' user_id='+str(uid)
    query = query + ' AND module_id='+str(module)
    query = query + ' AND target_type='+str(target_type)
#   if action!=0:
    #query = query + ' AND action!=0'
    query = query + ' ORDER BY target_id'
    result_list = db.queryDict(query)
    if len(result_list)>0:
        for result in result_list:
            _ids.append(result['target_id'])
    return _ids

def hasGlobalAccess(db,
                    uid,
                    module,
                    target_type):
    """
    """
    _result = getPermissions(db, uid, module, target_type, 0)
    return _result

def hasIdentifiedAccess(db,
                        uid,
                        module,
                        target_type):
    """
    """
    _result = 0
    query = 'SELECT action FROM ACL WHERE'
    query = query + ' user_id='+str(uid)
    query = query + ' AND module_id='+str(module)
    query = query + ' AND target_type='+str(target_type)
    query = query + ' AND target_id!=0'
    result_list = db.queryDict(query)
    if len(result_list)>0:
        _result = len(result_dict)
    return _result

def grant(  db,
            uid,
            module,
            target_type,
            target_id,
            action):
    """
    """
    
    _already_exist = False
    _is_similar = False
    # Checking if no permission has already been set
    query = 'SELECT action FROM ACL WHERE'
    query = query + ' user_id='+str(uid)
    query = query + ' AND module_id='+str(module)
    query = query + ' AND target_type='+str(target_type)
    query = query + ' AND target_id='+str(target_id)
    result_list = db.queryDict(query)
    if len(result_list)>0:
        _already_exist = True
        result_dict = result_list[0]
        _action = result_dict['action']
        if _action == action:
            _is_similar = True
            return
    if _already_exist == True:
        query = 'UPDATE ACL SET '
        query = query + 'action=' + str(action)
        query = query + ' WHERE '
        query = query + ' user_id='+str(uid)
        query = query + ' AND module_id='+str(module)
        query = query + ' AND target_type='+str(target_type)
        query = query + ' AND target_id='+str(target_id)
    else:
        query = 'INSERT INTO ACL(user_id, module_id, target_type, target_id, action) VALUES('
        query = query + str(uid) + ', ' + str(module) + ', ' + str(target_type) + ', '
        query = query + str(target_id) + ', ' + str(action) + ')'
    db.runQueryCommit(query)

def revoke( db,
            uid,
            module,
            target_type,
            target_id):
    """
    """

    query = 'DELETE FROM ACL WHERE '
    query = query + ' user_id='+str(uid)
    query = query + ' AND module_id='+str(module)
    query = query + ' AND target_type='+str(target_type)
    query = query + ' AND target_id='+str(target_id)
    db.runQueryCommit(query)
