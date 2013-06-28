from datadiff import diff
from django.shortcuts import render_to_response, get_object_or_404
import csv
import json
import os
import re,copy
from itertools import cycle
import collections
import urllib
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
    
    res=formatData2(lst)
    #res=json.dumps(res)
    print res
    
    
    params={
            'list':lst,
            'data':res,
            'voice': voice.replace("_"," ")
            }
    
    #return render_to_response('wikitoc/result.html',params)
    return params

def formatData(lst):
    
   
    lst.append([0,0,0,"0","0","0"])
    
    names=list()
    
    
    for l in lst:
        if l[3] in names:
            pass
        else:
            names.append(l[3])
    
    print names
    res=list()
            
    for n in names:
        
        currRev=lst[0][5]
        col=list()
        check = False
        
        for l in lst:
            if currRev==l[5] and n == l[3]:
                nth=dict()
                nth['rev']=l[0]
                nth['x']=l[5]
                nth['y']=l[4]
                nth['label'] = l[3]
                col.append(nth.copy())
                check=True
                
            elif currRev!=l[5] and n ==l[3]:
                nth=dict()
                nth['rev']=l[0]
                nth['x']=l[5]
                nth['y']=l[4]
                nth['label'] = l[3]
                currRev=l[5]
                col.append(nth.copy())
                check=True
                
            elif currRev==[5] and n !=l[3]:      
                continue
            
            elif currRev!=l[5] and n !=l[3] and not check:
                
                nth=dict()
                nth['rev']=l[0]
                nth['x']=currRev
                nth['y']=0
                nth['label'] = n
                currRev=l[5]
                col.append(nth.copy())
                
            elif currRev!=l[5] and n !=l[3] and check:
                currRev=l[5]
                check=False
            
        res.append(copy.copy(col))
    res.pop()
    return res

   
def formatData2(lst):
    
    names=list()
    res=list()
    
    for l in lst:
        if l[3] in names:
            pass
        else:
            names.append(l[3])
    
    values = sorted(set(map(lambda x:x[0], lst)),reverse=True)
    newlist = [[y for y in lst if y[0]==x] for x in values]  
    
    for n in names:
        
        namelist=list()
        
        for r in newlist:
            check=False
            
            for sr in r:
                
                if(sr[3])==n and not check:
                    nth=dict()
                    nth['rev']=sr[0]
                    nth['x']=sr[5]
                    nth['y']=sr[4]
                    nth['label'] = sr[3]
                    namelist.append(nth.copy())
                    check=True
                    
                elif (sr[3])==n and check:
                    pass
                
                    
            if not check:
                nth=dict()
                nth['rev']=sr[0]
                nth['x']=sr[5]
                nth['y']=0
                nth['label'] = n
                namelist.append(nth.copy())
            
        
        res.append(namelist)
    
    
    res.pop()
    print res
    return res

def tocLength(a,b):
	if len(a['sections']) != len(b['sections']):
		return True
	else:
		return False



