import datetime

from billy.scrape import NoDataForPeriod
from billy.scrape.agendas import AgendaScraper, Agenda

import lxml.html
import pytz
import requests
from bs4 import BeautifulSoup

class SDCCAgendaScraper(AgendaScraper):
    jurisdiction = 'citysd'
    
    _tz = pytz.timezone('US/Pacific')

    def scrape(self, chamber, session):
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
            
                when = "%s" % (date)
                when = datetime.datetime.strptime(when,
                                              "%Y-%M-%d")
                when = self._tz.localize(when)

                desc = title 
                #agenda = div.xpath("string(span[3])").strip()
                # XXX: Process `agenda' for related bills.
                agenda = Agenda(session, when, 'council:meeting',desc,
                                location=None)
                agenda.add_source(url)

                # desc is actually the ctty name.
                #event.add_participant('host', desc, 'committee',
                #                        chamber=chamber)

                self.save_agenda(agenda)
