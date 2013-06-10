from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from scripts.toc_scraper import scrapeTocs

from bootstrap_toolkit.widgets import BootstrapUneditableInput

from .forms import TestForm

def index(request):
    
    layout = 'inline'
    
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid(): # All validation rules pass
            message = form.cleaned_data['URL']
            message=message.split("/")[-1]
            return HttpResponseRedirect('/wikitoc/'+message) # Redirect after POST
    else:
        form = TestForm()
    
    return render_to_response('wikitoc/index.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))
    
def lookup(request, voice):
    
    scrapeTocs(voice)
    return HttpResponse(voice)
    