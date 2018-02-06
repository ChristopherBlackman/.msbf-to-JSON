import json
import dicttoxml
import xmltodict
import requests
import re
import untangle

from pprint import pprint
from bs4 import BeautifulSoup


FILE = "something.json"

def get_id(name):
    query = "https://myanimelist.net/search/all?q={}".format(name)

    for i in range(5):
        try:
            r = requests.get(query)
            soup = BeautifulSoup(r.text,'html.parser')
            firstMangaElement =  soup.find(id='manga').find_next().a['href']
            manga_id = re.search('(?<=/)\d+(?=/)',firstMangaElement).group(0)
            print(manga_id)
            return manga_id
        except AttributeError:
            print('AttributeError - {}'.format(name))
def main(): 

    p = Parser(FILE)
    p.getData() 

    a = AnimeListManga()
    a.getData()

    for item_obj in p.parsedItems():
        print "*"*30
        pprint(item_obj)
        pprint(a.find_closest_match(item_obj['name']))
        print "*"*30
        
    pass

class AnimeListFactory():
    def create_list_object(status,name):
        item = {}
        item['chapter'] = ''
        item['volume'] = ''
        item['status'] = ''
        item['score'] = ''
        item['times_reread'] = ''
        item['date_start'] = ''
        item['date_finish'] = ''
        item['priority'] = ''
        item['enable_discussion'] = ''
        item['enable_rereading'] = ''
        item['comments'] = ''
        item['scan_group'] = ''
        item['tags'] = ''
        item['retail_volumes'] = ''
        return item
 
class AnimeListManga():
    def __init__(self):
        self.url = "https://myanimelist.net/sitemap/manga-000.xml"
        self.data_base = list()


    def getData(self):
        r = requests.get(self.url)

        url = re.compile(r"(?<=<loc>)\S+(?=</loc>)")
        manga_id = re.compile('(?<=/)\d+(?=/)')
        name = re.compile('(?<=\d/)\S+$')
        for item in url.findall(r.content):
            try:
                item_obj = {}
                item_obj['id'] = manga_id.findall(item)[0]
                item_obj['name'] = name.findall(item)[0]
                self.data_base.append(item_obj)
            except IndexError:
                pprint('Invalid Item - {}'.format(item))
                continue

    def find_closest_match(self,name):
        i = 0
        current = None
        for item in self.data_base:

            set1 = set(name.lower().split('_'))
            set2 = set(item['name'].lower().split('_'))

            ji = self.compute_jaccard_sim(set1,set2)
            if ji > i:
                i = ji
                current = item
        return current
                

    def compute_jaccard_sim(self,set_1, set_2):
        n = len(set_1.intersection(set_2))
        return (n / float(len(set_1) + len(set_2) - n))



class Parser:
    def __init__(self,f_path):
        self.f_path = f_path
        self.data = None

    def getData(self):
        with open(self.f_path,'r') as f:
            self.data = json.loads(f.read())

    def parsedItems(self):
        for item_obj in self.data:
            item = {}
            item['name'] = item_obj[1].replace(' ','_')
            item['status'] = item_obj[3]
            yield item
main()
