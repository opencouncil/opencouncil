# -*- coding: utf-8 -*-
import re
import collections
from operator import methodcaller

import lxml.html

import scrapelib
from billy.scrape.committees import CommitteeScraper, Committee

class CitySDCommitteeScraper(CommitteeScraper):

    jurisdiction = 'citysd'
    
    url = "http://www.sandiego.gov/city-clerk/officialdocs/legisdocs/cccmeetings.shtml"

    def scrape(self, chamber, term):
        html = self.urlopen(self.url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(self.url)
        current_committees = doc.xpath('//h4')
        for c in current_committees:
            name = c.text_content()
            if name.startswith("Past") == False:
                c = Committee(chamber, name, short_name=name,
                          subcommittee=name)
                self.save_committee(c)
        past_committees = doc.xpath('//h5')
        for c in past_committees:
            name = c.text_content()
            c = Committee(chamber, name, short_name=name,
                          subcommittee=name)
            self.save_committee(c)  
