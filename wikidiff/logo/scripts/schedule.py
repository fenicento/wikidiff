from celery import task, current_task
from celery.result import AsyncResult
import requests, re, mechanize, json


@task(name='tasks.trends')
def scrapeTrends(q1,q2,q3):
    
    baseurl="http://www.google.com/trends/fetchComponent"
    
    
    
    
    
    payload={
            'q':q1,
            "cid":"TIMESERIES_GRAPH_0",
            "export":"3",
            "date" : "today 1-m"
            }
    
    cookies={
             'PREF':'ID=8dcb6a2c303edd4b:FF=0:LD=it:TM=1372346013:LM=1372346013:GM=1:S=_-xDOG-sqsDHYKfx'
             }
    
    headers={
             'Cookie':'PREF=ID=8dcb6a2c303edd4b:FF=0:LD=it:TM=1372346013:LM=1372346013:GM=1:S=_-xDOG-sqsDHYKfx',
             'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Encoding':'gzip,deflate,sdch',
             'Accept-Language':'en-US,en;q=0.8',
             'Cache-Control':'max-age=0',
             'Connection':'keep-alive'

             }
    

    
    r = requests.get(baseurl, params=payload, cookies=cookies, headers=headers )

    outer = re.compile("\((.+)\)")
    m = outer.search(r.text)
    inner_str = m.group(1)
    
    inner = re.compile("(new Date\(.+?\))")
    m =re.sub("(new Date\(.+?\))","\"\"",inner_str)
    
    a=json.loads(m)
    
    tab=a['table']['rows']
    
    for c in tab:
        print c['c']
    
    
    #br = mechanize.Browser()
    #br.open("http://www.google.com/trends/fetchComponent?q=ortona&cid=TIMESERIES_GRAPH_0&export=3")
    #response=br.response()
    #print response.read()
    
    