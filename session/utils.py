# -*- coding: utf_8 -*-

import md5, time, random

def create_id(seed = "spiff me up, dude!"):
    _hash = md5.new()
    _hash.update(seed)
    _hash.update(str(time.time()))
    _hash.update(str(random.random()))
    _id = _hash.hexdigest()
    return _id
