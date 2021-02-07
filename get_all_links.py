import fire
from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import re
from operator import iconcat
from itertools import chain

def get_all_links(url):
    soup = BeautifulSoup(
        urlopen(Request(url)),
        'lxml'
    )

    try:
        return list(map(
            lambda x: re.sub(r'\s', '+', str(x.get('href'))),
            soup.find_all('a')
        ))

    except urllib.error.HTTPError as err:
        print(f'{err} [{err.geturl()}]')

def walk_ftp_links(
        root_link,
        step,
        leaves_only = False,
        pred = lambda _: True
):
    results = []
    for link in get_all_links(root_link):
        full_link = root_link + link

        if link != '/' and not link.startswith('/ftp/') and not link.startswith('?') and link[-1] == '/':
            if not leaves_only and pred(full_link):
                results.append(step(full_link))

            results += walk_ftp_links(full_link, step, leaves_only, pred)

        else:
            if pred(full_link):
                results.append(step(full_link))

    return results

def get_all_ly_links(mutopia_homepage='https://www.mutopiaproject.org/ftp/'):
    soup = BeautifulSoup(
        urlopen(Request(mutopia_homepage))
    )

    ly_file_links = walk_ftp_links(
        leaves_only = True,
        pred = lambda lnk: '.ly' in lnk or '-ly' in lnk,
        step = print,
        root_link = mutopia_homepage
    )

def cli():
    fire.Fire(get_all_ly_links)
