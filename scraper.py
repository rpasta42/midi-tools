#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests, sys, re
from scrap_config import *
from utiltools import shellutils as shu

#https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
requests.adapters.DEFAULT_RETRIES = REQUESTS_NUM_RETRIES

def dw_url(url):
   resp = requests.get(url, timeout=REQUESTS_TIMEOUT)
   if resp.status_code is not 200:
      return None #raise "Bad response"
   else:
      return resp.content


def fix_link(link, parsed_url):
   '''Convert relative links to absolute

   parsed_url is is output of urllib.parse.urlparse() of URL on which the link is found'''

   if link is None:
      return None
   if any(key in link for key in ['http://', 'https://']) or len(link) == 0:
      return link

   #link == /blah or url is site root
   if link[0] == '/' or parsed_url.path == '':
      if link[0] == '/':
         link = link[1:]
      scheme = parsed_url.scheme + '://'
      return urljoin(scheme + parsed_url.netloc + '/', link).replace('/#', '#')

   full_original_url = parsed_url.geturl()

   #fix_link('test2', urlparse('test.com/blah/test.html')) should return test.com/blah/test2
   web_dir = '/'.join(full_original_url.split('/')[:-1])
   return web_dir + '/' + link


def get_page_re_links(page_text, parsed_url):
   '''Beautiful soup didn't find browsehappy.com so using the regex version for that'''
   href_regex = '''href=['|"]([^'"]*)['|"]'''
   links = [fix_link(link, parsed_url) for link in re.findall(href_regex, page_text)]
   links = filter(lambda link: not any(key in link for key in ['css', '.png', '.ico']), links)
   return list(links)


def get_page_links(soup, parsed_url):
   a_tags = soup.find_all('a')
   links = [fix_link(tag.get('href'), parsed_url) for tag in a_tags]
   links = list(filter(lambda x: x != None, links))
   return links

def get_page_title(soup):
   return soup.title.getText()


def scrape(url, page_content=None):

   parsed_url = urlparse(url)

   if page_content is None:
      page_content = dw_url(url)
   if page_content is None:
      print('Could not download the page')
      return None

   soup = BeautifulSoup(page_content, 'html.parser')
   #print(soup.prettify())

   page_title = get_page_title(soup)
   page_soup_links = get_page_links(soup, parsed_url)
   page_re_links = get_page_re_links(str(page_content), parsed_url)

   page_links = list(set(page_soup_links + page_re_links))

   return page_title, page_links


def dw_song(link, i, tot):
   song_name = link.split('/')[-1]
   song_name_clean = song_name.\
            replace('(', '__OP__').\
            replace(')', '__CP__').\
            replace('[', '__OB__').\
            replace(']', '__CB__').\
            replace('(c)', 'C')

   print('[%i/%i] %s' % (i, tot, link))

   song_resp = requests.get(link)
   if song_resp.status_code != 200:
      print('bad song failed (%s)\n\t%s' % (song_name_clean, link))

   song_data = song_resp.content
   shu.write_file('songs/' + song_name_clean, song_data, binary=True)

   pass

def dw_songs(links):

   shu.mkdir('songs')

   good_links = []
   for link in links:
      if link.split('.')[-1] in ['mid', 'midi']:
         good_links.append(link)
      pass

   for i, link in enumerate(good_links):
      dw_song(link, i, len(good_links))

   print('bad links', set(links) - set(good_links))
   pass



if __name__ == '__main__':
   #test_url = 'http://www.kunstderfuge.com/mozart.htm'
   test_url = 'http://midiworld.com/mozart.htm'
   if len(sys.argv) > 1:
      test_url = sys.argv[1]

   title, links = scrape(test_url)
   dw_songs(links)

   print('Title:', title)
   for link in links:
      print(link)


