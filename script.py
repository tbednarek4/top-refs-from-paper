import requests
from collections import Counter
from prettytable import PrettyTable

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
