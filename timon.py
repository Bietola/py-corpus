from collections import defaultdict
import re
from typing import Dict, List
from pathlib import Path
import emoji

from utils import eprint

def parse_tierlist(tierlist: List[str]) -> Dict[str, str]: 
    tier_re = re.compile(r'^##\s*(.*)$')
    card_re = re.compile(r'^-\s*(.*)$')

    result = {}
    curr_tier = "N/A"
    lnum = 1
    for line in tierlist:
        line = line.strip()

        if m := tier_re.match(line):
            tier = m.group(1)

            curr_tier = tier

            lnum = 1

        elif m := card_re.match(line):
            card = m.group(1)

            tier_num = ""
            if curr_tier == "Garbage":
                tier_num = ' ' + emoji.emojize(':hankey: ' * lnum)
            else:
                tier_num = str(lnum)
            result[card.lower()] = curr_tier + tier_num

            lnum += 1

        else:
            eprint("{}".format(line))

    return result

def get_timon_tierlist():
    if not get_timon_tierlist.cache:
        tierlist = Path("timon-tier-list.md").read_text()
        get_timon_tierlist.cache = parse_tierlist(tierlist.split('\n'))

    return get_timon_tierlist.cache
get_timon_tierlist.cache = None

def get_tier(card):
    return get_timon_tierlist().get(card.lower(), 'N/A')
