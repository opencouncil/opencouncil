import re
from operator import methodcaller

import lxml.html

from billy.scrape.legislators import LegislatorScraper, Legislator

class OceansideLegislatorScraper(LegislatorScraper):

    jurisdiction = 'oceanside'
    base_url = 'http://www.ci.oceanside.ca.us'
    legislators_url = base_url + "/gov/council/default.asp"
    
    def scrape(self, chamber, term):
        html = self.urlopen(self.legislators_url)
        doc = lxml.html.fromstring(html)
        cells = doc.xpath('//table/tbody/tr/td')
        for cell in cells:
            cell_xpath = cell.xpath
            res = {}
            res['full_name'] = cell_xpath('a')[0].text_content()
            res['email'] = cell_xpath('a/@href')[1].replace('mailto:','')
            res['title'] = cell_xpath('text()')[0].strip()
            res['phone'] = cell_xpath('text()')[1].strip()
            res['url'] = self.base_url + cell_xpath('a/@href')[0]
            leg = Legislator(term, chamber, 'district', **res)
            print leg
            leg.update(**res)
            self.save_legislator( leg ) 
