#!/usr/bin/python

__description__ = 'Grab files from Google of a certain file type'
__author__ = 'Brandon Dixon'
__version__ = '1.0'
__date__ = '2010/11/21'

import optparse
import urllib
import simplejson
import random
import os

def download_file(file_name,file_mode,base_url,out):
	from urllib2 import Request, urlopen, URLError, HTTPError

	#create the url and the request
	url = base_url
	req = Request(url)

	# Open the url
	try:
		f = urlopen(req)
		print "downloading " + url

		# Open our local file for writing
		if out != "":
			local_file = open(out + file_name, "w" + file_mode)
		else:
			local_file = open(file_name, "w" + file_mode)

		#Write to our local file
		local_file.write(f.read())
		local_file.close()

	#handle errors
	except HTTPError, e:
		print "HTTP Error:",e.code , url
	except URLError, e:
		print "URL Error:",e.reason , url

def random_word(filename):
    filesize = os.stat(filename)[6]
    fd = file(filename,'rb')
    for _ in range(10) : # Try 10 times
        pos = random.randint(0,filesize)
        fd.seek(pos)
        fd.readline()  # Read and ignore
        line = fd.readline()
    if line != '' :
        return line

def random_start():
    value = random.randrange(0, 15, 5)
    return value

def grab_files(urls, out):
	print "====== DOWNLOADING FILES ======"
	count = 0
	for url in urls:
		parts = url.split("/")
		filename = parts[-1]
		download_file(filename,"b",url,out)
		count+=1
    
	print "%d files downloaded" % (count)

def get_urls(file_type="pdf", amount=10, search="query", randomq=False):
    count = 0
    url_list = []
    runtime = amount / 5

    while count < runtime:
        
        start = random_start()
        if randomq == True:
            search = random_word('dictionary.txt')

        #construct the query
        ip = str(random.randrange(1,254)) + "." + str(random.randrange(1,254)) + "." + str(random.randrange(1,254)) + "." + str(random.randrange(1,254))
        query = urllib.urlencode({'q' : '%s filetype:%s' % (search, file_type)})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&userip=%s&rsz=5&start=%s&%s' % (ip,start,query)
        print "====== Seed Query: " + query + " ====="
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        results = json['responseData']['results']
        for i in results:
            url_list.append(i['url'])
        count+=1
    return url_list
    
def main():
    oParser = optparse.OptionParser(usage='usage: %prog [options]\n' + __description__, version='%prog ' + __version__)
    oParser.add_option('-t', '--type', type='string', help='filetype to download')
    oParser.add_option('-a', '--amount', default='10', type='int', help='amount of files to download')
    oParser.add_option('-q', '--query', default='', type='string', help='search value')
    oParser.add_option('-r', '--random', action='store_true', default=False, help='file full of random search values')
    oParser.add_option('-o', '--out', default='', type='string', help='output directory')
    (options, args) = oParser.parse_args()

    if options.type:
        urls = get_urls(options.type, options.amount, options.query, options.random)
        grab_files(urls, options.out)
    else:
        oParser.print_help()
        return

if __name__ == '__main__':
    main()
