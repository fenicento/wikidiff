from datadiff import diff
from django.shortcuts import render_to_response, get_object_or_404
import csv
import json
import os
import re,copy
from itertools import cycle
import collections
import urllib, datetime
from dateutil import parser
import datetime
from math import fabs
from operator import itemgetter
#encoding= utf-8



def compareTocs(listing,voice):
	listcycle = cycle(listing)
	nextelem = listcycle.next()
	
	collection = []
	
	
	for thiselem in listing:
		
		
		thiselem, nextelem = nextelem, listcycle.next()
		if nextelem == listing[0]:
			pass
		else:
			rev_1 = thiselem
			rev_2 = nextelem
			
			
			#print tocLength(rev_1,rev_2)
	        if tocLength(rev_1,rev_2):
	            if len(rev_1['sections'])>0:
	                revId = rev_1['revid']
	                ts=rev_1['timestamp']
	                
	                ind0=0
	                num0=0
	                offset0=int(rev_1['sections'][0]['byteoffset'])
	                name0='intro'
	                collection.append({'revId':revId, 'ind':ind0, 'num':num0, 'tocName':name0, 'offset':offset0,'ts':ts})
	                
	                for index, s in enumerate(rev_1['sections']):
	                   
	                    tocName = s['line']
	                    tocName=tocName.encode('utf8')
	                    ind=s['index']
	                    anchor=s['anchor']
	                    num=s['number']
	                    try:
	                        offset = int(rev_1['sections'][int(index)+1]['byteoffset']) - int(s['byteoffset'])
	                        
	                    except Exception, err:
	                        offset = int(rev_1['size'])-int(s['byteoffset'])
	
	                    collection.append({'revId':revId, 'ind':ind, 'num':num, 'tocName':tocName, 'anchor':anchor, 'offset':offset,'ts':ts})
	                
	                print revId
	            
	        else:
	            list_1 = []
	            list_2 = []
	            for index, s in enumerate(rev_1['sections']):
	                list_1.append([index, s['anchor'], s['number']])
	            for index, s in enumerate(rev_2['sections']):
	                list_2.append([index, s['anchor'], s['number']])
	            if list_1 == list_2:
	                continue
	            elif(len(rev_1['sections'])>0):
	                revId = rev_1['revid']
	                ts=rev_1['timestamp']
	                
	                ind0=0
	                num0=0
	                offset0=int(rev_1['sections'][0]['byteoffset'])
	                name0='intro'
	                collection.append({'revId':revId, 'ind':ind0, 'num':num0, 'tocName':name0, 'offset':offset0,'ts':ts})
	                
	                for index, s in enumerate(rev_1['sections']):
	                    tocName = s['line']
	                    tocName=tocName.encode('utf8')
	                    ind=s['index']
	                    anchor=s['anchor']
	                    num=s['number']
	                    try:
	                        offset = int(rev_1['sections'][int(index)+1]['byteoffset']) - int(s['byteoffset'])
	                        
	                        print "*************************"
	                        
	                    except Exception, err:
	                        print err
	                        offset = int(rev_1['size'])-int(s['byteoffset'])
	                        print "#########################"
	                    collection.append({'revId':revId, 'ind':ind, 'num':num, 'anchor':anchor,'tocName':tocName, 'offset':offset,'ts':ts})
	                print revId
	
	return lookup(collection,voice)

def lookup(lst,voice):    
    
    res,longest,oldest,newest,overlapping=formatData2(lst)
    #res=json.dumps(res)
    
    params={
            'data':res,
            'list':lst,
            'longest':longest,
            'oldest':newest,
            'newest':oldest,
            'days':overlapping,
            'voice': voice.replace("_"," ")
            }
    #return render_to_response('wikitoc/result.html',params)
    return params


def formatData2(lst):
    
    names=list()
    res=list()
    
    
    for l in lst:
        
        if l['tocName'] in names:
            pass
        else:
            names.append(l['tocName'])
    
    values = sorted(set(map(lambda x:x['revId'], lst)),reverse=True)
    
    newlist = [[y for y in lst if y['revId']==x] for x in values]  
    
    
    longest=0
    oldest=datetime.datetime(1970,2,11,20,0,0,0)
    newest=datetime.datetime.now()
    previous=oldest
    overlapping=0
    days=0
    i=0
    
    newlist.sort(comparator)
    
    for ind,n in enumerate(newlist):
        g=0
        prevOffset=0
        prevOverlap=0
        
        #questa parte va ad un livello superiore!!!!!  
        if(i>0):  
     
            
            previous=parser.parse(newlist[i-1][0]['ts'])
            actual=parser.parse(n[0]['ts'][:10])
          
            delta=actual-previous
            days=fabs(delta.days)
            overlapping=overlapping+days
   
        
        for m in n:
            
            if(ind<len(newlist)-1):
                
                try:
                    pind=map(itemgetter('tocName'), newlist[ind+1]).index(m['tocName'])
                    m['change']=-(newlist[ind+1][pind]['offset']-m['offset'])
                except:
                    m['new']=True
                    
            if(ind>0):
                try:
                    pind=map(itemgetter('tocName'), newlist[ind-1]).index(m['tocName'])
                except:
                    m['last']=True
                
            
            g=g+m['offset']
            m['y']=i
            m['ts']=m['ts'][:10]
            m['days']=days
            m['start']=prevOffset
            d=parser.parse(m['ts'])
        
            if d<newest:
                newest=d
            if d>oldest:
                oldest=d
            
            
            prevOffset=prevOffset+m['offset']

        if g>longest:
            longest=g
            
        
        
        i=i+1

    return newlist,longest,oldest.strftime("%Y-%m-%d"),newest.strftime("%Y-%m-%d"), overlapping

def tocLength(a,b):
	if len(a['sections']) != len(b['sections']):
		return True
	else:
		return False

def comparator(x, y):
    
    a=parser.parse(x[0]['ts'])
    b=parser.parse(y[0]['ts'])
    d=b-a
    print "seconds:"
    print d.seconds
    return int(d.total_seconds())

