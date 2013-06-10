from datadiff import diff
import csv
import json
import os
from itertools import cycle
import collections

#folder = 'toc/Family_planning/'
folder = 'toc/Birth_control/'
os.chdir(folder)

listing = filter(os.path.isfile, os.listdir('.'))
listing = [os.path.join('.', f) for f in listing] # add path to each file
listing.sort(key=lambda x: os.path.getmtime(x))

listcycle = cycle(listing)
nextelem = listcycle.next()

def tocLength(a,b):
	if len(a['sections']) != len(b['sections']):
		return True
	else:
		return False

collection = []


for thiselem in listing:
	thiselem, nextelem = nextelem, listcycle.next()
	if nextelem == listing[0]:
		pass
	else:
		rev_1 = open(thiselem)
		rev_1 = json.load(rev_1)
		rev_2 = open(nextelem)
		rev_2 = json.load(rev_2)
		
		#print tocLength(rev_1,rev_2)
		if tocLength(rev_1,rev_2):
			revId = rev_1['revid']
			prevByteOffset = 0
			for index, s in enumerate(rev_1['sections']):
				tocName = s['anchor']
				offset = int(s['byteoffset'])
				offset = offset - prevByteOffset
				prevByteOffset =int(s['byteoffset'])
				collection.append([revId, tocName, offset])
			print revId
		else:
			list_1 = []
			list_2 = []
			for index, s in enumerate(rev_1['sections']):
				list_1.append([index, s['anchor'], s['number']])
			for index, s in enumerate(rev_2['sections']):
				list_2.append([index, s['anchor'], s['number']])
			if list_1 == list_2:
				pass
			else:
				revId = rev_1['revid']
				prevByteOffset = 0
				for index, s in enumerate(rev_1['sections']):
					tocName = s['anchor']
					offset = int(s['byteoffset'])
					offset = offset - prevByteOffset
					prevByteOffset =int(s['byteoffset'])
					collection.append([revId, tocName, offset])
				print revId

headers = ['revId', 'tocName', 'tocLength']
writer = csv.writer(open('toc_change_rev_new.tsv', 'wb'), delimiter='\t', quotechar='"')
writer.writerow(headers)
writer.writerows(collection)

# for i in [i for i,x in enumerate(rev_2['sections'])]:
# 	print i, x['anchor']
	
# for index, s in enumerate(rev_2['sections']):
#     print index, s['anchor'], s['number']
#     
# for index, s in enumerate(rev_1['sections']):
#     print index, s['anchor'], s['number']
	
# for i in [i for i,x in enumerate(rev_2['sections']) if x['anchor'] == 'Modern_methods']:
# 	print i
	

#tocLength(rev_1,rev_2)
#compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
