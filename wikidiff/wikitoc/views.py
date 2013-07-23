from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from scripts.toc_scraper import scrapeTocs
from scripts.toc_scraper2 import scrapeTocs2
from scripts.toc_compare import compareTocs
from scripts.toc_compare2 import compareTocs2
import re,json, copy
from celery import task, current_task
from celery.result import AsyncResult
import pprint
from dateutil import parser
import datetime
from math import fabs
from operator import itemgetter

from bootstrap_toolkit.widgets import BootstrapUneditableInput

from .forms import TestForm


def index(request):
    
    layout = 'inline'
    
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid(): # All validation rules pass
            message = form.cleaned_data['URL']
            lang=re.search('http://(.+?)\.', message).group(1)
            print lang
            message=message.split("/")[-1]
            #return HttpResponseRedirect('/wikitoc/lookup/'+message+"?lang="+lang) # Redirect after POST
            job=scrapeTocs.apply_async((message, lang))
            params={
                    "job":job.id
                    }
            return render_to_response('wikitoc/result.html',params)
    else:
        form = TestForm()
    
    return render_to_response('wikitoc/index.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


    
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
    pp = pprint.PrettyPrinter(indent=4)
    
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

def comparator(x, y):
    
    a=parser.parse(x[0]['ts'])
    b=parser.parse(y[0]['ts'])
    d=b-a
    print "seconds:"
    print d.seconds
    return int(d.total_seconds())

def example(request, voice):
    
    lst=compareTocs2(voice)
    voice.replace("_"," ")
    res,longest,oldest,newest,overlapping=formatData2(lst)
    params={
            'list':lst,
            'data':json.dumps(res),
            'longest':longest,
            'oldest':oldest,
            'newest':newest,
            'days':overlapping,
            'voice': voice
            }
   
    return render_to_response('wikitoc/example.html',params)
    

def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state
    return HttpResponse(json.dumps(data), mimetype='application/json')


def init_work(request, voice):
    """ A view to start a background job and redirect to the status page """
    lang=request.GET.get('lang')
    job=scrapeTocs.apply_async((voice, lang))
    params={
            "job":job.id
            }
    return render_to_response('wikitoc/result.html',params)

def startJob(voice, lang):
    """ A view to start a background job and redirect to the status page """
    job=scrapeTocs.apply_async((voice, lang))
    params={
            "job":job.id
            }
    return render_to_response('wikitoc/result.html',params)
    
    