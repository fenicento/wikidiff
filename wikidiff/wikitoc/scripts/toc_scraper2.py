import urllib
import csv
import json
import sys
from toc_compare import compareTocs
from toc_compare2 import compareTocs2
import re
import urllib
import os
#encoding= utf-8

baseUrl= 'http://en.wikipedia.org/w/api.php?'
revisionsTot = []
lst=[]
curpath = os.path.abspath(os.curdir)

def scrapeTocs2(voice,lang):
    
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
            f = open(curpath+"/wikitoc/scripts/Family_planning/" + title + "_" + str(revId[0]) + ".json","w+")
            f.write(json.dumps(output,sort_keys=False, indent=4))
            
            
        except Exception, e:
            print "Unexpected error:", e
    
    res = compareTocs2(lst);
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
            revScraper(params)
        except Exception, e:
            print e, 'ho finito di cercare le revision ids'
    
    except Exception, e:
        print "Unexpected error:", e
    
