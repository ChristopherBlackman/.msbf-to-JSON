import json
import dicttoxml
import xmltodict
import requests
import re
import untangle
import editdistance

from pprint import pprint
from bs4 import BeautifulSoup
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

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

def get_alternatives(url):
    alt = None
    syn = None
    titles = list()

    m = re.compile('(?<=Synonyms:</span>)[\s\d\w,]+')
    p = re.compile('(?<=</span>)[\s\d\w,]+')


    print url
    for i in range(5):
        soup = None
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text,'html.parser')

            alt =  soup.find_all('h2',text='Alternative Titles')[0].find_next()
            syn =  soup.find_all('h2',text='Alternative Titles')[0].find_next().parent()
        except Exception:
            print 'sss'
            continue
            pass

        try:
            synynomes = map(str.strip,m.findall(str(syn))[0].split(','))
            titles = list(set(list(synynomes)+titles))
        except Exception:
            pass

        try:
            alterante =  alt.text.replace('English:','').strip()
            titles = list(set(synynomes+titles))
        except:
            pass
        break
    return titles



def w_shingles(word,w):
    items = []
    for i in range(0,max(len(word)-w+1,0)):
        items.append(word[i:i+w])

    return set(items)

def main(): 

    p = Parser(FILE)
    p.getData() 

    a = AnimeListManga()
    a.getData()

    for item_obj in p.parsedItems():
        match = a.find_closest_match(item_obj['name'])
        print match
        
    pass
 
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
                #print get_alternatives(item)
                item_obj = {}
                item_obj['id'] = manga_id.findall(item)[0]
                item_obj['name'] = name.findall(item)[0]
                self.data_base.append(item_obj)
            except IndexError:
                pprint('Invalid Item - {}'.format(item))
                continue

    def find_closest_match(self,name,n=5,p=.10):
        i = 0
        obj = {}
        for item in self.data_base:

            name2 = item['name'].encode('ascii','ignore')

            #print(type(name2))
            set1 = w_shingles(name.lower(),n)
            set2 = w_shingles(name2.lower(),n)

            ji = self.compute_jaccard_sim(set1,set2)
            if ji > max(i,p):
                i = ji
                obj['name'] = item['name']
                obj['id'] = item['id']
                obj['js'] = ji
                obj['search-key'] = name


        return obj
                

    def compute_jaccard_sim(self,set_1, set_2):
        n = len(set_1.intersection(set_2))
        r = float(len(set_1) + len(set_2) - n)
        if r == 0:
            return 0
        return (n /r)



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
#print get_alternatives('https://myanimelist.net/manga/2/Berserk')
#get_alternatives('https://myanimelist.net/anime/8516/Baka_to_Test_to_Shoukanjuu_Ni')
