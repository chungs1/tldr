"""else:
            details = tag.text.encode('utf-8')\
                      .strip().replace('\xc2\xa0', '').replace('\xe2\x80\x93', '-').split("\n")      
            printText(details)"""

from bs4 import BeautifulSoup, NavigableString
import urllib, urllib2, sys, re
import webbrowser
from random import choice
from tf_idf import *

#gives the delimiters
extra = ["'", '"', ',', ':', ')', '(', '=', '-',
         '_', '+', '*', '&', '^', '%', '$', '#', '@', '!', '<', '>',
         '}', '{', '[', ']', '`', '`', "/", ";"]

#finds the sentence enders
sentenceend = re.compile('[.?!]')

#creates a random user agent so able to use with restricted websites
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

class MyOpener(urllib.FancyURLopener, object):
    version = choice(user_agents)

#create instance of opener.
myopener = MyOpener()

base = 'http://'

url = raw_input('Your url, please: ')
def make_url():
    
    if 'http://' not in url and 'https://' not in url:
        #print('ok')
        if ' ' in url:
            url = url.replace(' ', '')
        url = base + url
        #print(url)
    return scrape_info(url)


def scrape_info(url):
    scraped = ''
    final_scrape = ''
    avg_score = 0
    total_score = 0
    
    try:
        #gives the array of the strings in each div
        response = myopener.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        soup.prettify()
        results = soup.findAll("p")
        results = filter(visible, results)
        result = printText(soup.findAll("p"))

        #compiles into a single string
        for scrape in result:
            for letter in scrape:
                scraped += letter
                #print(scraped)
            scraped += ' '
            scraped += '| '

        #gets rid of extra
        for aletter in scraped:
            if aletter in extra:
                scraped = scraped.replace(aletter, '')

        #finds the average weight of entire
        weight_dict = word_weight(scraped)
        text = scraped.split('.')
        for string in text:
            length = len(string.split())
            splitted = string.split()
            for word in splitted:
                total_score += weight_dict[word]
                avg_score += total_score
            total_score = 0
        m = len(text)
        if len(text)<=0:
            m = 1
        avg_score = avg_score / (m-.99999999)
        print(avg_score)

        #get the weight of each word, then eval
        for string in text:
            length = len(string.split())
            for word in string.split():
                total_score += weight_dict[word]
            if length == 0:
                length = 1
            if total_score >= avg_score/length:
                final_scrape += string
                final_scrape += '.'
            total_score = 0

        """#getting rid of end paragraphs.
        count = 0
        for i, another_letter in enumerate(final_scrape):
            if another_letter == "|":
                count += 1
        if count >= 5:
            new_count = 0
            for x, omgz_letter in enumerate(final_scrape):
                while new_count <= 5:
                    if another_letter == '|':
                        new_count += 1
                    if new_count == 5:
                        final_scrape = final_scrape[:x+1]
                        return printing(final_scrape)"""
        #adding paragraphs
        for another_letter in final_scrape:
            if another_letter == '|':
                final_scrape = final_scrape.replace('|', '\n\n')
        return final_scrape
        #print(final_scrape)
        

    except urllib2.HTTPError as err:
        print(err.code)
        if err.code == 404:
            print(err)
        if err.code == 403:
            print err.fp.read()
        else:
            raise
    except IOError as e:
        print(e)
        print('No connection established. Try again after your connection has stabilized or choose a different url')        
    #except Exception as e:
        #print(e)

def printText(tags):
    stfu = []
    for tag in tags:
        if tag.__class__ == NavigableString:
            print(tag)
        else:
            details = tag.text.encode('utf-8')\
                      .strip().replace('\xc2\xa0', '').replace('\xe2\x80\x93', '-')\
                      .replace("\'s", "'s").replace('\xe2\x80\x94', '--')\
                      .split("\n")
            stfu.append(details)
            #print(tag)
    return stfu

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def printing(final_scrape):
    #adding paragraphs
    for another_letter in final_scrape:
        if another_letter == '|':
            final_scrape = final_scrape.replace('|', '\n\n')
                    
    return final_scrape

    
            

#make_url(url)
