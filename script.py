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
  
import re, requests
from bs4 import BeautifulSoup
from collections import Counter
from prettytable import PrettyTable

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')\

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def get_pdf(doi_link, filename):
  response = requests.get(f'https://sci-hub.ru/{doi_link}')
  soup = BeautifulSoup(response.content, 'lxml')
  papers = soup.find_all('embed')[0].get('src').rsplit('#', 1)[0]
  
  with open(filename, 'wb') as f:
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

def get_title(doi_link):
  response = requests.get(f'https://api.crossref.org/works/{doi_link}')
  output = cleanhtml(response.json().get('message', {}).get('title')[0])
  return output

def get_most_popular_refs(first_link):
  first_list = get_references(first_link)
  second_list = sum([ get_references(link) for link in first_list if get_references(link) ], [])

  res = Counter(second_list).most_common()

  my_table = PrettyTable()
  my_table.field_names = ["Count", "DOI", "Title"]

  for doi, count in res[:50]:
    title = get_titles(doi)
    my_table.add_row([count, doi, title])
  
  print(my_table)
  pass
