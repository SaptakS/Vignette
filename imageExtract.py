import json
import os
import re
import time
import urllib2
import requests
from BeautifulSoup import BeautifulSoup
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError

def go(query, path):
  """Download full size images from Google image search.
  Don't print or republish images without permission.
  I used this to train a learning algorithm.
  """
  BASE_PATH = os.path.join(path, query)
  query = query.replace(' ', '%%20')
  BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
             'v=1.0&q=' + query + '&start=%d'


  

  if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

  start = 0 # Google's start query string parameter for pagination.
  img_title = 1
  while start < 60: # Google will only return a max of 56 results.
    r = requests.get(BASE_URL % start,)
    for image_info in json.loads(r.text)['responseData']['results']:
      url = image_info['unescapedUrl']
      try:
        image_r = requests.get(url)
      except ConnectionError, e:
        print 'could not download %s' % url
        continue

      # Remove file-system path characters from name.
      title = image_info['titleNoFormatting'].replace('/', '').replace('\\', '').replace('.','').replace('|','')

      file = open(os.path.join(BASE_PATH, '%s.jpg') % img_title, 'wb')
      img_title = img_title + 1
      try:
        Image.open(StringIO(image_r.content)).save(file, 'JPEG')
      except IOError, e:
        # Throw away some gifs...blegh.
        print 'could not save %s' % url
        continue
      finally:
        file.close()

    print start
    start += 4 # 4 images per page.

    # Be nice to Google and they'll be nice back :)
    time.sleep(1.5)

#the main part of the script
url_painter = "http://www.thefamouspeople.com/painters.php"
request = urllib2.Request(url_painter)
pagehtml = urllib2.urlopen(request).read()
data = BeautifulSoup("".join(pagehtml))
painters = data.findAll("a", {"class":"btn btn-primary btn-sm btn-block btn-block-margin"})
#print painters
for painter in painters:
    painter = "".join(painter)
    painter = "".join(re.split(r">|<",painter))+" painting"
    #print painter
    try:
        go(painter,'imageDB')
        print "Done ",painter
    except ValueError, e:
        print "could not find"
        continue
    


#for painter_info i json.loads(website.text)[]
'''
# Example use
#go('pablo picaso paintings', 'imageDB')
