import fire
import re
from sys import stderr
from cardinality import count

# TODO: zips_always_come_first = False
def remove_expanded_zips(links_file, zips_always_come_first=True):
    with open(links_file, 'r') as f:
        links = f.readlines()

    if not zips_always_come_first:
        assert False, "Not implemented yet"

    zip_link_re = re.compile(r'^(.*?)\.zip$')
    subpaths_re = re.compile(r'(.*?)\/')

    zip_folder_links = set()
    for link in links:
        print(f'Processing {link}', file=stderr) # DB

        if m := zip_link_re.match(link):
            print(f'Zip match: {link}', file=stderr) # DB

            sublink = m.group(1)
            zip_folder_links.add(sublink)

            print(link, end='')

        else:
            is_zip_folder_link = count(filter(
                lambda zfl: zfl in link,
                zip_folder_links
            )) >= 1

            if not is_zip_folder_link:
                print(link, end='')

def cli():
    fire.Fire(remove_expanded_zips)
