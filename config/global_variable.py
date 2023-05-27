def init_var():
    global var_list
    var_list = {}


def read_basic_config():
    import ujson
    with open('/config.json', 'r') as f:
        config = f.read()
        config = ujson.loads(config)
    set_var('ssid', config['Network_Config']['ssid'])
    set_var('password', config['Network_Config']['password'])
    set_var('device_id', config['Device_Config']['id'])
    set_var('device_name', config['Device_Config']['name'])
    set_var('server', config['Server_Config']['server'])
    set_var('port', config['Server_Config']['port'])
    set_var('connect_username', config['Server_Config']['user'])
    set_var('connect_password', config['Server_Config']['password'])


def set_var(key, value):
    var_list[key] = value


def getvalue(key):
    if key in var_list:
        return var_list[key]
    else:
        return None


def remove_var(key):
    var_list.pop(key)
