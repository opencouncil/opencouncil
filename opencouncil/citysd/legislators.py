import re
from operator import methodcaller

import lxml.html

from billy.scrape.legislators import LegislatorScraper, Legislator

titles = ['Vacant', 'Councilmember', 'Council President Pro Tem', 'Council President']

class CitySDLegislatorScraper(LegislatorScraper):

    jurisdiction = 'citysd'
    base_url = 'http://www.sandiego.gov/'
    legislators_url = base_url + '/citycouncil/'
    
    def scrape(self, chamber, term):
        html = self.urlopen(self.legislators_url)
        doc = lxml.html.fromstring(html)
        members = doc.xpath('//div[@id="cdlist"]/div[@class="cd"]')
        for member in members:
            member_xpath = member.xpath
            res = {}

            title_name = member_xpath('div[@class="cdinfo"]/text()')[0].strip()
            res['url'] = self.base_url + member_xpath('div[@class="cdinfo"]/a/@href')[0]
            district = member_xpath('div[@class="cdinfo"]/a')[0].text_content().strip()
            if len(member_xpath('div[@class="cdinfo"]/a')) > 1:
                res['email'] = member_xpath('div[@class="cdinfo"]/a')[1].text_content().strip()
            else:
                res['email'] = None
            for t in titles:
                if t in title_name:
                    res['title'] = t
                    res['full_name'] = title_name.replace(t, '').strip()

            leg = Legislator(term, chamber, district, **res)
            leg.update(**res)
            self.save_legislator( leg )
