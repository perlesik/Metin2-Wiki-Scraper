from bs4 import BeautifulSoup
import requests
import re
from get_links import generate_links


def get_info_from_tag(tag):
    regex = re.search(">(.*)<", str(tag))
    return regex.group(1)


def get_tags(soup_obj):
    # Checks if there's Karty Potwora system and sets table number accordingly.
    if soup_obj.find('img', attrs={'alt': 'Karta Potwora default.png'}):
        table_num = 2
    else:
        table_num = 1
    nt = soup_obj.select(f'#mw-content-text > .mw-parser-output > table:nth-of-type({table_num}) > tbody > '
                        'tr:nth-of-type(1) > td:nth-of-type(1) > b:nth-of-type(1)')
    lt = soup_obj.select(f'#mw-content-text > .mw-parser-output > table:nth-of-type({table_num}) > tbody > '
                        'tr:nth-of-type(3) > td:nth-of-type(2) > div:nth-of-type(2)')
    gt = soup_obj.select(f'#mw-content-text > .mw-parser-output > table:nth-of-type({table_num}) > tbody > '
                        'tr:nth-of-type(3) > td:nth-of-type(2) > div:nth-of-type(4)')
    return nt, lt, gt


def get_monster_info(monster_url):
    r = requests.get(monster_url)
    soup = BeautifulSoup(r.content, "html.parser")
    name_tag, lvl_tag, grade_tag = get_tags(soup)

    n = get_info_from_tag(name_tag)
    lv = get_info_from_tag(lvl_tag)
    g = get_info_from_tag(grade_tag)

    return n, lv, g


monster_info = []
if input("Generate links? ") == 'y':
    generate_links()

with open('links.txt', 'r') as file:
    for link in file:
        link_fixed = link.strip()
        name, lvl, grade = get_monster_info(link_fixed)
        monster_info.append(f"{name};{lvl};{grade}")
        print(f"Nazwa: {name}, poziom: {lvl}, stopień: {grade}")

with open('monster_info.txt', 'w') as m_file:
    for line in monster_info:
        m_file.write(f"{line}\n")
