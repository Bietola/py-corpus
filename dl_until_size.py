import fire
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen, urlretrieve
import sys
from sys import stderr
from pathlib import Path

def last_subpath(path):
    return path.split('/')[-1].strip()

def dl_until_size(links_file, max_tot_size_mb, target='.'):
    target = Path(target)

    def clean_link_contents(contents):
        # return '\n'.join(filter(
        #     lambda line: not line.isspace(),
        #     contents.split('\n')
        # ))

        # TODO: Transform tabs into spaces
        return contents

    with open(links_file) as f:
        links = f.readlines()

    total_size = 0
    for idx, link in enumerate(links):
        if total_size >= max_tot_size_mb * 1024 * 1024:
            break

        # TODO: Look inside zips
        if '.zip' in link:
            continue

        dl_file_name = f'{idx}-{last_subpath(link)}'
        with open(target / Path(dl_file_name), 'w') as f:
            print(f'Downloading {link} in {dl_file_name}', file=stderr)

            link_contents = urlopen(links[0]).read().decode('utf-8')

            link_contents = clean_link_contents(link_contents)

            dl_size = sys.getsizeof(link_contents)
            total_size += dl_size

            print(f'Download finished; size: {dl_size}B; tot: {total_size}B', file=stderr)

            f.write(link_contents)

    print(f'All downloads finished; tot: {total_size / 1024 / 1024}MB', file=stderr)

def cli():
    fire.Fire(dl_until_size)
