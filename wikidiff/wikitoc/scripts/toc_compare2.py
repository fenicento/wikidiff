from datadiff import diff
import csv
import json
import os
from itertools import cycle
import collections
import urllib
#encoding= utf-8

curpath = os.path.abspath(os.curdir)

def compareTocs2():
    
    folder = curpath+"/wikitoc/scripts/Family_planning/"
    os.chdir(folder)

    listing = filter(os.path.isfile, os.listdir('.'))
    listing = [os.path.join('.', f) for f in listing] # add path to each file
    listing.sort(key=lambda x: os.path.getmtime(x))
    
    listcycle = cycle(listing)
    nextelem = listcycle.next()
    
    collection = []
    
    
    for thiselem in listing:
        
        
        thiselem, nextelem = nextelem, listcycle.next()
        if nextelem == listing[0]:
            continue
        else:
            rev_1 = open(thiselem)
            rev_1 = json.load(rev_1)
            rev_2 = open(nextelem)
            rev_2 = json.load(rev_2)
            
            
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
    
    return collection

def tocLength(a,b):
    if len(a['sections']) != len(b['sections']):
        return True
    else:
        return False



#headers = ['revId', 'tocName', 'tocLength']
#writer = csv.writer(open('toc_change_rev_new.tsv', 'wb'), delimiter='\t', quotechar='"')
#writer.writerow(headers)
#writer.writerows(collection)

# for i in [i for i,x in enumerate(rev_2['sections'])]:
#     print i, x['anchor']
    
# for index, s in enumerate(rev_2['sections']):
#     print index, s['anchor'], s['number']
#     
# for index, s in enumerate(rev_1['sections']):
#     print index, s['anchor'], s['number']
    
# for i in [i for i,x in enumerate(rev_2['sections']) if x['anchor'] == 'Modern_methods']:
#     print i
    

#tocLength(rev_1,rev_2)
#compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
