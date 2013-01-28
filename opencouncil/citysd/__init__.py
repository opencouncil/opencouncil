import datetime
import lxml.html

metadata = dict(
    name='City of San Diego',
    abbreviation='citysd',
    capitol_timezone='US/Pacific',
    legislature_name='San Diego City Council',
    chambers = {
        'upper': {'name': 'Council', 'title': 'Councilmember'},
    },
    terms=[
        {'name': '2011-2012', 'start_year': 2011,
         'end_year': 2012, 'sessions': ['2011', '2012']},
        {'name': '2013-2014', 'start_year': 2013,
         'end_year': 2014, 'sessions': ['2013']},
        ],
    session_details={
        '2011': {'start_date': datetime.date(2011, 1, 5),
                 'display_name': '2011 Regular Session',
                 '_scraped_name': '2011 Regular Session',
                },
        '2012': {'display_name': '2012 Regular Session',
                 '_scraped_name': '2012 Regular Session',},
        '2013': {'display_name': '2013 Regular Session',
                 '_scraped_name': '2013 Regular Session',},
        },
        feature_flags=[],
  _ignored_scraped_sessions = [
        '2013',
        '2012',
        '2011',
        '2010',
        ]
)

def session_list():
    from billy.scrape.utils import url_xpath
    import re
    #sessions = url_xpath('http://www.sandiego.gov//city-clerk/officialdocs/legisdocs/previous.shtml',
    #    "//select[@name='a']/option/text()")
    sessions = ['2013','2012','2011','2010']
    return sessions


def extract_text(doc, data):
    doc = lxml.html.fromstring(data)
    divs_to_try = ['//div[@id="bill"]', '//div[@id="bill_all"]']
    for xpath in divs_to_try:
        div = doc.xpath(xpath)
        if div:
            return div[0].text_content()
