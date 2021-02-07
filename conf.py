from utils import eprint

_conf = {}

# TODO: Use configuration file
_conf['chat_names'] = {
    # 669174061: 'admin'
}

def get(conf_opt):
    # TODO: Use configuration file
    if conf_opt == 'admin_chat_id':
        return None

    conf_item =_conf[conf_opt]
    if conf_item != None:
        return conf_item
    else:
        eprint(f'Error: no {conf_opt} provided in configuration file')
        return None
