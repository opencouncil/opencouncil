import re
from operator import methodcaller

import lxml.html

from billy.scrape.legislators import LegislatorScraper, Legislator

titles = ['Chair', 'Vice Chair'], 

class CountySDLegislatorScraper(LegislatorScraper):

    jurisdiction = 'countysd'
    base_url = 'http://www.sdcounty.ca.gov/'
    legislators_url = base_url + 'general/bos.html'
    
    def scrape(self, chamber, term):
        if chamber == 'lower':
            return
        html = self.urlopen(self.legislators_url)
        doc = lxml.html.fromstring(html)
        table  = doc.xpath('//table')[27]
        row = table.xpath('tr')[1]
        members = row.xpath('td')
        for member in members:
            res = {}
            member_xpath = member.xpath
            name = member_xpath('span/b/a/text()')
            if name:
                res['full_name'] = name[0]
            else:
                res['full_name'] = member_xpath('a/span/b/text()')[0].strip()
            res['url'] = member_xpath('span/a/@href')[0].strip()
            district = member_xpath('span/a')[0].text_content().strip()
            title_el = member_xpath('span/a/text()')
            if len(title_el) > 1:
                res['title'] = title_el[1].strip()
            else:
                res['title'] = ""
            leg = Legislator(term, chamber, district, **res)
            leg.update(**res)
            self.save_legislator( leg )
