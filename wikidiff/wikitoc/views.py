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
    
    