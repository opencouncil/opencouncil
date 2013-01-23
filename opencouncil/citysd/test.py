import re
import requests
from bs4 import BeautifulSoup

base_url = "http://dockets.sandiego.gov/sirepub/"

def bs_preprocess(html): 
     """remove distracting whitespaces and newline characters""" 
     pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE) 
     html = re.sub(pat, '', html)       # remove leading and trailing whitespaces 
     html = re.sub('\n', ' ', html)     # convert newlines to spaces 
                                        # this preserves newline delimiters 
     html = re.sub('[\s]+<', '<', html) # remove whitespaces before opening tags 
     html = re.sub('>[\s]+', '>', html) # remove whitespaces after closing tags 
     return html 

def process_url(url):
    r = requests.get(url)
    print url, r.status_code
    soup = BeautifulSoup(r.text)
    form_inputs = soup.form.find_all('input')
    for input in form_inputs:
        if input.get('id') == "lefturlval":
            lefturlval = base_url + input.get('value')
            #print lefturlval
            r2 = requests.get(lefturlval)
            if r2.status_code == 200:
                doc_soup = BeautifulSoup(bs_preprocess(r2.text))
                span = doc_soup.span
                if span.text and span.text !="The file could not be found or is not available at this time.  Please try again later.":
                    ps = doc_soup.find_all('p')
                    for p in ps:
                        if p.text.replace('*','').replace(' ', '').startswith('ITEM-'):
                            item = p.text.strip().replace('* ', '')
                            parts = item.split(":")
                            print parts[0].strip(), parts[1].strip()

#for meeting_id in range(1438,1439):
    #agenda_url = ('%spubmtgframe.aspx?meetid=%d&doctype=Agenda' % (base_url, meeting_id))
    #process_url(agenda_url)
    #minutes_url = ('%spubmtgframe.aspx?meetid=%d&doctype=Minutes' % (base_url, meeting_id))
    #process_url(minutes_url)
    #summary_url = ('%spubmtgframe.aspx?meetid=%d&doctype=Summary' % (base_url, meeting_id))
    #process_url(summary_url)


def check_agendas():
    r = requests.get("http://google.sannet.gov/search?num=100&requiredfields=PATH:councildockets|PATH:councilminutes|PATH:councilresults&getfields=DOCUMENT_URL.DOC_DATE.TITLE.SORTORDER&sort=date:D:S:d1&output=xml_no_dtd&ie=UTF-8&client=scs_ocd&filter=0&site=documents&config=sirecouncilmeetings.js&proxystylesheet=sirefrontend&q=Council+inmeta:DOC_DATE_NUM:20130101..20140101")
    soup = BeautifulSoup(r.text)
    table = soup.find_all('table')[-1]
    rows = table.findAll('tr')
    for row in rows:
        date_cell = row.findAll('script')[0].text
        if date_cell.startswith('build_date_cell'):
            date = date_cell[17:27]
            link = row.find('a')
            url = link['href']
            title = link.text
            print date, url, title


check_agendas()
