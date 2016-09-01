from urllib2 import urlopen
from bs4 import BeautifulSoup
import pprint
from re import search

def same_domain(url):
    return search('^\/([\w\.\/]*)?', url) is not None

def visit(url, domain, visited, master_list):
    #import ipdb; ipdb.set_trace()
    if not visited.has_key(url):
        visited[url] = True #if key does not exist, then set value to true because it will be visited now
    elif visited.has_key(url) and visited[url] is False:
        visited[url] = True #if key exists and its false for whatever reason
    else:
        return True #key exists and its already visited

    print 'Visiting:',url
    try:
        soup = BeautifulSoup(urlopen(domain+url), 'lxml')
    except:
        print 'Woops! Probs a 404:',url
        return 'yo'

    links = soup('a')
    master_list = master_list.union(links)
    links = filter(lambda l: l['href'] if l.has_attr('href') else False, links)
    links = map(lambda l: l['href'], links)
    links = set(links) #de-dupes
    links = filter(same_domain, links) #remove links outside of current domain 
    links = filter(lambda l: (visited.has_key(l) and not visited[l]) or not visited.has_key(l), links)
    for link in links:
        visit(link, domain, visited, master_list)

domain = 'http://www.codingdojo.com'

visited = {}
master = set()

visit('/', domain, visited, master)
print visited
