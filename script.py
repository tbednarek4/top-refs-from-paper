# top-refs-from-paper: simple Python script to retrieve the citations from Crossref API
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

import requests
from collections import Counter
from prettytable import PrettyTable
from bs4 import BeautifulSoup

def download_pdf(doi_link):
  response = requests.get(f'https://sci-hub.ru/{doi_link}')
  soup = BeautifulSoup(response.content, 'lxml')
  papers = soup.find_all('embed')[0].get('src').rsplit('#', 1)[0]

  with open('temp.pdf', 'wb') as f:
      f.write(requests.get(f'https://sci-hub.ru/{papers}').content)
      return True
    
  return False

def get_references(doi_link):
  response = requests.get(f'https://api.crossref.org/works/{doi_link}')
  output = response.json().get('message', {}).get('reference')

  if output != None:
    ref_list = [ el.get('DOI') for el in output if el.get('DOI') ]
    return ref_list
  else: pass

def get_titles(doi_link):
  response = requests.get(f'https://api.crossref.org/works/{doi_link}')
  output = response.json().get('message', {}).get('title')
  return output

def get_most_popular_refs(first_link):
  first_list = get_references(first_link)
  second_list = sum([ get_references(link) for link in first_list if get_references(link) ], [])

  res = Counter(second_list).most_common()

  my_table = PrettyTable()
  my_table.field_names = ["Count", "Title", "DOI"]

  for doi, count in res[:50]:
    title = get_titles(doi)
    my_table.add_row([count, doi, title])
  
  print(my_table)
  pass

if __name__ == '__main__':
  test_link_01 = '10.1002/anie.202013801'
  test_link_02 = '10.1021/acscatal.8b02371'
  get_most_popular_refs(test_link_01) 
  get_most_popular_refs(test_link_02)
