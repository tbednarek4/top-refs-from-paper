# top-refs-from-paper: retrieve top citations from a scientific paper using Crossref
# Copyright (C) 2023 Tomasz Bednarek

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from collections import Counter
from time import perf_counter, sleep
import argparse, json, os, pip, re

before = perf_counter()

def install(package):
  pip.main(['install', package])

def install_all_packages(modules_to_try):
  os.system('python -m pip install --upgrade pip > $null')
  for module in modules_to_try:
    try:
      __import__(module)        
    except ImportError as e:
      install(e.name)

install_all_packages(['bs4', 'prettytable', 'requests'])
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

flag = True
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def get_pdf(doi_link, filename):
  response = None

  try:
    response = requests.get(f'https://api.crossref.org/works/{doi_link}')
  except TimeoutError:
    print(f'Timeout for {doi_link}')
    sleep(60)
    return get_pdf(doi_link, filename)

  soup = BeautifulSoup(response.content, 'lxml')
  papers = soup.find_all('embed')[0].get('src').rsplit('#', 1)[0]
  
  with open(filename, 'wb') as f:
    f.write(requests.get(f'https://sci-hub.ru/{papers}').content)
    return True
  return False

def get_references(doi_link):
  response = None

  try:
    flag = True
    response = requests.get(f'https://api.crossref.org/works/{doi_link}')
  except TimeoutError:
    print(f'Timeout for {doi_link}')
    sleep(60)
    if flag: 
      flag = False
      return get_references(doi_link)
    else: exit()

  output = None

  try: 
    output = response.json().get('message', {}).get('reference')
  except json.decoder.JSONDecodeError:
    print(f"There is a problem with JSON output from DOI: {doi_link}")
    pass

  if output != None:
    ref_list = [ el.get('DOI') for el in output if el.get('DOI') ]
    return ref_list
  else: pass

def get_title(doi_link):
  response = None
  output = None
  
  try:
    flag = True
    response = requests.get(f'https://api.crossref.org/works/{doi_link}')
  except TimeoutError:
    print(f'Timeout for {doi_link}')
    sleep(60)
    if flag: 
      flag = False
      return get_references(doi_link)
    else: exit()

  try: 
    output = cleanhtml(response.json().get('message', {}).get('title')[0])
  except json.decoder.JSONDecodeError:
    print(f"There is a problem with title retrival from DOI: {doi_link}")
    pass

  return output

def get_ranking(temp_set, depth, previous_list=[]):
  next_list = []
  for link in temp_set:
    temp = get_references(link)
    if temp: next_list.extend(temp)
    else: print(f'References not found for {link}')

  next_set = set(next_list)
  next_list.extend(previous_list)

  if depth > 1:
    get_ranking(next_set, depth - 1, next_list)
  else:
    res = Counter(next_list).most_common()
    my_table = PrettyTable()
    my_table.field_names = ["Count", "DOI", "Title"]

    for doi, count in res[:100]:
      title = get_title(doi)
      if title: my_table.add_row([count, doi, title])

    print('\n')
    print(my_table)
    pass  

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--doi', type=str, help='DOI link input', required=True)
  parser.add_argument('--depth', type=int, help='Depth of the ranking', required=True)
  args = parser.parse_args()

  temp_set = set([args.doi])
  get_ranking(temp_set, args.depth)
  after = perf_counter()
  print(f"\nExecution time: {after - before} s\n")
