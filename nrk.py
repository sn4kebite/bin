#!/usr/bin/env python2

import sys, urllib2
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup

parser = OptionParser()
parser.add_option('-s', '--speed', type = 'int', help = 'Bitrate speed in Kbps', default = 2000)
parser.add_option('-e', '--execute', help = 'Command to exec()', default = None)

(options, args) = parser.parse_args()

if len(args) < 1:
	print('Usage: {0} URL'.format(sys.argv[0]))
	sys.exit(1)

req = urllib2.Request(args[0], headers = {'Cookie': 'NetTV2.0Speed={0}'.format(options.speed)})
doc = urllib2.urlopen(req).read()

soup = BeautifulSoup(doc)

# fetch the embed with our url
embed = soup.find('embed', attrs = {'type': 'application/x-mplayer2'})
if not embed:
	print('No embed found! Invalid link?')
	sys.exit(2)

# fetch url
src = embed.get('src')
# split out the browser argument
url = src.rsplit('&browser', 1)[0]

if options.execute:
	import os
	os.execvp(options.execute.split()[0], [arg.format(url = url) for arg in options.execute.split()])
else:
	print(url)
