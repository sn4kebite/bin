#!/usr/bin/env python2

import sys, urllib2, re
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup

class M3U8Error(Exception): pass

class M3U8(object):
	def __init__(self, f):
		self.read(f)

	def read(self, f):
		self.items = []
		line = f.readline()
		if not line.startswith('#EXTM3U'):
			raise M3U8Error()
		while not line.startswith('#EXTINF') and not line.startswith('#EXT-X-STREAM-INF'):
			line = f.readline().strip()
		while line:
			if line.startswith('#EXT-X-STREAM-INF'):
				meta = line.split(':', 1)[-1]
				m = re.findall(r'([^=,]+)=(?:"([^"]*)"|([^,]*))', meta)
				meta = dict((i[0], i[1] or i[2]) for i in m)
				url = f.readline().strip()
				self.items.append((url, meta))
			elif line.startswith('#EXTINF'):
				meta = {}
				url = f.readline().strip()
				self.items.append((url, meta))
			line = f.readline().strip()

parser = OptionParser()
parser.add_option('-e', '--execute', help = 'Command to exec()', default = None)

(options, args) = parser.parse_args()

if len(args) < 1:
	print('Usage: {0} URL'.format(sys.argv[0]))
	sys.exit(1)

req = urllib2.Request(args[0])
req.add_header('Cookies', 'NRK_PROGRAMPLAYER_SETTINGS=devicetype=desktop&preferred-player-odm=hlslink&preferred-player-live=hlslink&max-data-rate=5000')
doc = urllib2.urlopen(req).read()
open('data', 'w').write(doc)

soup = BeautifulSoup(doc)

playerdiv = soup.find('div', attrs = {'id': 'playerelement'})
if not playerdiv:
	print('No embed found! Invalid link?')
	sys.exit(2)

playlist = playerdiv.get('data-media')

playlist = playlist.replace('/z/', '/i/')
playlist = playlist.rsplit('/', 1)[0] + '/index_4_av.m3u8'

req = urllib2.Request(playlist)
playlist = urllib2.urlopen(req)

playlist = M3U8(playlist)
print '\n'.join(item[0] for item in playlist.items)

#if options.execute:
#	import os
#	os.execvp(options.execute.split()[0], [arg.format(url = url) for arg in options.execute.split()])
#else:
#	print(url)
