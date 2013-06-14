from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from scripts.toc_scraper import scrapeTocs
import re,json, copy

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
            return HttpResponseRedirect('/wikitoc/lookup/'+message+"?lang="+lang) # Redirect after POST
    else:
        form = TestForm()
    
    return render_to_response('wikitoc/index.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))
    
def lookup(request, voice):
    
    lang=request.GET.get('lang')
    lst = scrapeTocs(voice,lang)
    res=formatData(lst)
    res=json.dumps(res)
    
    params={
            'list':lst,
            'data':res,
            'voice': voice.replace("_"," ")
            }
    
    return render_to_response('wikitoc/result.html',params)

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
    
    # for l in lst:
#         
        # if l[5]!=currRev:
            # res.append(entry.copy())
            # entry=dict()
            # entry['timestamp']=l[5]
            # entry[l[3]]=l[4]
            # currRev=l[5]
#             
        # else:
            # entry[l[3]]=l[4]
            
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
    
    
    
    