from typing import List, NewType, Callable

from mex.utils import eprint, remove_common_prefix
import mex.dotted_dict as dotkey
from mex.val import *

#########
# Types #
#########

Scope = NewType("Scope", List[str])
Path = NewType("Path", str)

####################
# Helper Functions #
####################

def flatten_dict(init, lkey='', separator='.', key_mask=lambda e: e):
    ret = {}
    for rkey,val in init.items():
        key = lkey + rkey

        if isinstance(val, dict) and not key_mask(key):
            ret.update(flatten_dict(val, key + separator))
        else:
            ret[key] = val
    return ret

def scopify(dotted_str):
    return dotted_str.split('.')

def add_scope(scope: Scope, s: Path) -> Path:
    if len(s) == 0:
        return '.'.join(scope)

    if len(scope) == 0:
        return s

    return '.'.join(scope) + '.' + s

def add_scope_rel(scope: Scope, s, starting_path):
    abs_s = scopify(add_scope(scope, s))

    rel_s, nic = tuple(map(list, remove_common_prefix(abs_s, scopify(starting_path)))) # nic: not in common

    lvs_to_go_back = len(nic)
    rel_pre = ['<..>'] * lvs_to_go_back
    rel_s = add_scope(rel_pre, '.'.join(rel_s))

    return rel_s

def expand_path(scope: Scope, path) -> Path:
    if len(path) == 0:
        return path

    if path[0] == '.':
        return add_scope(scope, path[1:])

    return path

##################
# Helper Classes #
##################

class TravConf:
    trav_map: Callable

    def __init__(self, trav_map):
        self.trav_map = trav_map

#################
# Context class #
#################

class Context:
    ret = None

    scope: Scope
    env = {}
    cur_item = None

    def __init__(self, cur_item, scope=[], env={}, cached_exps={}):
        self.scope = scope
        self.env = env
        self.cached_exps = cached_exps
        self.cur_item = cur_item

    def _tree(self, root_path, tcfg: TravConf):
        root_path = expand_path(self.scope, root_path)

        root = dotkey.get(self.env, root_path)

        if not root:
            return {}

        # TODO: Figure this out (NB. Currently only works with '.' as root_path)
        # cur_item_rel2root = expand_path_rel(self.cur_item, root_path)
        cur_item_rel2root = self.cur_item.split('.')[-1]
        ret = { 
            k: v for (k, v)
            in map(
                tcfg.trav_map,
                map(
                    lambda x: (x[0], x[1].eval(x[0], scopify(root_path))),
                    root.items()
                )
            )
        }
        dotkey.pop(ret, cur_item_rel2root)

        return ret

    def _trav_flags(raw=1):
        trav_map = lambda x: x

        if raw == 1:
            # TODO: Use composition
            trav_map = lambda p: (p[0], p[1].raw())

            # This sickens me...
            # trav_map_res = lambda x: [ (p[0][0], p[0][1].raw())
            #     for p in [trav_map(x)]
            # ]

        return TravConf(
            trav_map
        )

    def tree(self, root_path, **kwargs):
        return self._tree(root_path, Context._trav_flags(**kwargs))

    def vtree(self, root_path, **kwargs):
        return list(flatten_dict(self.tree(root_path, **kwargs)).values())
