import urllib
import csv
import json
import sys
from toc_compare import compareTocs
from toc_compare2 import compareTocs2
from celery import task, current_task
from celery.result import AsyncResult
import re, time
import urllib
#encoding= utf-8

baseUrl= 'http://en.wikipedia.org/w/api.php?'
revisionsTot = []
lst=[]

@task(name='tasks.scrapeTocs')
def scrapeTocs(voice,lang):
	
	print lang
	
	bu=re.sub("en",lang,baseUrl)
	
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
					'rvprop': 'timestamp|ids|size',
					'format': 'json',
					'rvlimit': 'max'
				}
	
	#writer = csv.writer(open(title + '.tsv', 'wb'), delimiter='\t', quotechar='"')
	#headers=['timestamp', 'revision_id']
	#writer.writerow(headers)
	
	revScraper(params,bu)
	
	print 'Parto con i TOC'

	i = 0;
	
	start_time = time.time()
	
	for revId in revisionsTot:
		try:
			i=i+1
			
			print "parsing revision "+ str(i) + " of " + str(len(revisionsTot))
			
			# progInt=(i/len(revisionsTot))*30
			# progress="*" * int(progInt)
			# tot="_"*int(30-int(progInt))
# 			
# 			
			# print "progress: " + progress+tot
			
			paramsToc['oldid'] = revId[0]
			paramsEncoded = urllib.urlencode(paramsToc)
			f = urllib.urlopen(bu + "%s" %paramsEncoded)
			results = f.read()
			results = json.loads(results)
			output = results['parse']
			output['timestamp'] = revId[1]
			output['size'] = revId[2]
			
			
			
			lst.append(output)
			
			tot_t=time.time() - start_time
			uni_t=tot_t/i;
			rem_t=int(uni_t*(len(revisionsTot)-i))
			rem_str="";
			
			if rem_t>3600:
				h=int(rem_t/3600)
				m=int(rem_t/60-h*60)
				s=int(rem_t-m*60)
				rem_str="Approximately "+str(h)+" hours, "+str(m)+" minutes and "+str(s)+" seconds remaining"
			elif rem_t>60:
				m=int(rem_t/60)
				s=int(rem_t-m*60)
				rem_str="Approximately "+str(m)+" minutes and "+str(s)+" seconds remaining"
			else:
				rem_str="Approximately "+str(rem_t)+" seconds remaining"
			
			current_task.update_state(state='PROGRESS', meta={'current': i, 'total': len(revisionsTot),'time':rem_str})
			#f = open("toc/" + title + "_" + str(revId) + ".json","wb")
			#f.write(json.dumps(output,sort_keys=False, indent=4))
			
			
		except Exception, e:
			print "Unexpected error:", e
	
	res=compareTocs(lst,voice);
	
	return res

def revScraper(params, baseUrl):
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
				revision_size = revision['size']
				revisionsTot.append([revision_id,revision_timestamp,revision_size])
				
				#row = [revision_id, revision_timestamp]
				#writer.writerow(row)
		try:
			rvcontinue = results['query-continue']['revisions']['rvcontinue']
			params['rvcontinue'] = rvcontinue
			revScraper(params,baseUrl)
		except Exception, e:
			print e, 'ho finito di cercare le revision ids'
	
	except Exception, e:
		print "Unexpected error:", e

	