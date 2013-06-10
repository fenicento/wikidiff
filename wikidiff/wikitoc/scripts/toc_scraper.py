import urllib
import csv
import json
import sys

baseUrl= 'http://en.wikipedia.org/w/api.php?'
revisionsTot = []

def scrapeTocs(voice):
	
	rvcontinue= ''
	title = voice
	
	paramsToc = {  	
					'action':'parse',
					'prop':'sections',
					'page':title,
					'format': 'json',
					'oldid' : ''
				}
	
	params = {  	
					'action':'query',
					'prop':'revisions',
					'titles':title,
					'rvprop': 'timestamp|ids',
					'format': 'json',
					'rvlimit': 'max'
				}
	
	writer = csv.writer(open(title + '.tsv', 'wb'), delimiter='\t', quotechar='"')
	headers=['timestamp', 'revision_id']
	writer.writerow(headers)
	
	
	
	revScraper(params, writer)
	
	
	
	print 'Parto con i TOC'
	for revId in revisionsTot:
		try:
			print revId
			paramsToc['oldid'] = revId
			paramsEncoded = urllib.urlencode(paramsToc)
			f = urllib.urlopen(baseUrl + "%s" %paramsEncoded)
			results = f.read()
			results = json.loads(results)
			output = results['parse']
			f = open("toc/" + title + "_" + str(revId) + ".json","wb")
			f.write(json.dumps(output,sort_keys=False, indent=4))
	
			
		except Exception, e:
			print "Unexpected error:", e

def revScraper(params,writer):
	try:
		paramsEncoded = urllib.urlencode(params)
		f = urllib.urlopen(baseUrl + "%s" %paramsEncoded)
		results = f.read()
		results = json.loads(results)
		
		pages = results['query']['pages']
		pagesId = pages.keys()
		
		for pageId in pagesId:
			revisions = pages[pageId]['revisions']
			
			for revision in revisions:
				
				revision_id = revision['revid']
				revision_timestamp = revision['timestamp']
				revisionsTot.append(revision_id)
				row = [revision_id, revision_timestamp]
				writer.writerow(row)
		try:
			rvcontinue = results['query-continue']['revisions']['rvcontinue']
			params['rvcontinue'] = rvcontinue
			revScraper(params)
		except Exception, e:
			print e, 'ho finito di cercare le revision ids'
	
	except Exception, e:
		print "Unexpected error:", e
	
