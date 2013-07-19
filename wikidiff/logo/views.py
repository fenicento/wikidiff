# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from scripts.schedule import scrapeTrends
import json

def index(request):
    
    
    return render_to_response('logo/index.html')

def find(request):
    
    q=""
    
    if request.GET.get('q'):
        q=request.GET.get('q')
        
    else: 
        return "error"
    
    splitq=q.split(",")
    res=scrapeTrends(splitq[0],splitq[1],splitq[2],splitq[3])
    
    return HttpResponse(json.dumps(res), mimetype="application/json")
    
    