from bs4 import BeautifulSoup
import requests
import re
from areas import areas


def get_links(area_url):
    """Returns url links of monsters in area"""
    r = requests.get(area_url)
    soup = BeautifulSoup(r.content, "html.parser")
    links = str(
            soup.select('#mw-content-text > .mw-parser-output > table:nth-of-type(1) > tbody > tr:nth-of-type(4) > '
                            'td:nth-of-type(1) > table:nth-of-type(1) > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > '
                            'div:nth-of-type(1) > ul:nth-of-type(1) > li'))
    matches = re.findall('href="/index.php/(.*?)"', links, re.DOTALL)
    matches_fixed = []
    for count, value in enumerate(matches):
        if count % 2 == 0:
            matches_fixed.append(value)
    return matches_fixed


def get_monsters_from_all_areas():
    all_monsters = []
    for area_link in areas:
        area_list = get_links(area_link)
        all_monsters.extend(area_list)
    return all_monsters


def generate_links():
    monsters_names = get_monsters_from_all_areas()
    with open('links.txt', 'w') as file:
        for name in monsters_names:
            file.write(f"https://pl-wiki.metin2.gameforge.com/index.php/{name}\n")