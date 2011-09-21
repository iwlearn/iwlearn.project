import urllib, urllib2
import random
import logging

from BeautifulSoup import BeautifulSoup

from vocabulary import my_countrylist as _countrylist

logger = logging.getLogger('iwlearn.project')

def get_gef_iw_project_page(focalarea='I'):
    """
    http://www.gefonline.org/projectListSQL.cfm

    Parameters    application/x-www-form-urlencoded
    Bottom             -90
    Cmd                Map
    Left               -180
    OMEReports         All
    Random             705547512
    Right              180
    Search             dbsearch
    Top                83.6235961914063
    approvalEndDate
    approvalStartDate
    fipscode           All
    focalsearch        I/M
    format             gef
    fundsearch
    iasearch           All
    keysearch
    name               gef
    operator           less
    opsearch           All
    trustfundsearch    All
    typesearch         All

    returns a list of all gef IW projects
    """
    url = 'http://www.gefonline.org/projectListSQL.cfm'
    params = urllib.urlencode({
        'Cmd':  'Map',
        'Bottom':   '-90',
        'Top':  '90',
        'Left': '-180',
        'Right':    '180',
        'OMEReports':   'All',
        'Random':   str(random.randint(100000000, 999999999)),
        'Search':   'dbsearch',
        'approvalEndDate':  '',
        'approvalStartDate':  '',
        'fipscode': 'All',
        'focalsearch':  focalarea,
        'format':   'gef',
        'fundsearch':  '',
        'iasearch': 'All',
        'keysearch':  '',
        'name': 'gef',
        'operator': 'less',
        'opsearch': 'All',
        'trustfundsearch':  'All',
        'typesearch':   'All'
        })
    response = urllib2.urlopen(url, data=params)
    data = response.read()
    return data

def extract_gefids_from_page(data):
    """
    takes the html page from http://www.gefonline.org/projectListSQL.cfm
    and extracts the project ids.
    returns a list of all projectids (integer) on the page
    """
    prurl = 'projectDetailsSQL.cfm?projID='
    id_list = []
    soup = BeautifulSoup(data)
    for td in soup.findAll('td'):
        a = td.find('a')
        if a:
            atxt = a.getText()
            href=None
            for attr in a.attrs:
                if attr[0] == 'href':
                    href = attr[1]
                    if href.startswith(prurl):
                        gefid = href[len(prurl):]
            try:
                itxt = int(atxt)
                igefid = int(gefid)
            except ValueError:
                continue
            if itxt == igefid:
                id_list.append(itxt)
    return list(set(id_list))


def extract_project_info(gefid):
    """
    extracts the projectinfo from
    http://www.gefonline.org/projectDetailsSQL.cfm?projID=####
    and returns a dict of the extracted information
    """
    url = 'http://www.gefonline.org/projectDetailsSQL.cfm?projID=%i' % gefid
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        return {}
    soup = BeautifulSoup(response)
    project_data = {}
    for tr in soup.findAll('tr'):
        td = tr.findAll('td')
        if len(td) == 2:
            project_data[td[0].text] = td[1].text
    return project_data


GEF_PLONE_COUNTRY_MAPPING = {
    'Antigua And Barbuda' : 'Antigua and Barbuda',
    'Bosnia-Herzegovina' : 'Bosnia and Herzegovina',
    'Congo DR' : 'Congo The Democratic Republic of',
    'Iran': 'Iran Islamic Republic of',
    'Korea DPR': "Korea Democratic People's Republic of",
    'Lao PDR': "Lao People's Democratic Republic",
    'Libya': 'Libyan Arab Jamahiriya',
    'Macedonia': 'Macedonia the former Yugoslavian Republic of',
    'Micronesia': 'Micronesia Federated States of',
    'Moldova': 'Moldova Republic of',
    #'Montenegro': 'Serbia and Montenegro',
    'Palestinian Authority': 'Palestinian Territory occupied',
    'Republic Of Korea': 'Korea Republic of',
    'Serbia': 'Republic of Serbia',
    'Slovak Republic': 'Slovakia',
    'St. Kitts And Nevis': 'Saint Kitts and Nevis',
    'St. Lucia': 'Saint Lucia',
    'St. Vincent and Grenadines': 'Saint Vincent and the Grenadines',
    'Syria': 'Syrian Arab Republic',
    'Tanzania': 'Tanzania United Republic of',
    'Timor Leste': 'Timor-Leste',
    'Vietnam': 'Viet Nam',
    'Republic of Serbia': 'Serbia'
}

def convert_currency_to_millions(c_str):
    if c_str:
        try:
            return float(c_str[:-4].replace(',',''))/1000000
        except:
            return 0.0

def get_countries(c_str):
    def extract_countries(clist):
        plone_countries = [c['name'] for c in _countrylist.values()]
        countries = []
        _countries = [country.strip() for country in clist]
        for c in _countries:
            if GEF_PLONE_COUNTRY_MAPPING.has_key(c):
                country = GEF_PLONE_COUNTRY_MAPPING[c]
            else:
                country=c
            if country in plone_countries:
                countries.append(country)
            else:
                logger.info('Country [%s] ommitted' % country )
        return countries
    # main
    if c_str.find('(') > 1:
        cl = c_str[c_str.find('(') + 1 :c_str.find(')')].split(',')

    else:
        if c_str.find(',') > 1:
            cl = c_str.split(',')
        else:
            cl = [c_str]

    return list(set(extract_countries(cl)))

#XXX debug only
def get_all_projectinfo():
    """
    ['', 'PDF A Amount', 'Operational Program', 'GEF Project Grant (CEO Appr.)',
    'PDF-B (Supplemental-2) Approval Date', 'Project Cancellation Date',
    'PPG Amount', 'GEF Project ID', 'Cofinancing Total (CEO Endo.)',
    'GEF Agency Fees (CEO Endo.)', 'UNDP PMIS ID', 'Funding Source',
    'Executing Agency', 'PDF-C Approval Date', 'Project Name',
    'Project Completion Date', 'GEF Project Grant', 'Focal Area',
    'PIF Approval Date', 'Project Cost', 'Cofinancing Total (CEO Appr.)',
    'PDF-A Approval Date', 'PPG Approval Date', 'PRIF Amount', 'Country',
    'Region', 'PDF-B Approval Date', 'Implementation Status',
    'GEF Project Grant (CEO Endo.)', 'GEF Agency Fees', 'PDF B Amount',
    'GEF Grant', 'PDF C Amount', 'CEO Endorsement Date', 'Description',
    'GEF Agency', 'Pipeline Entry Date', 'Cofinancing Total',
    'Approval Date', 'Project Status', 'PDF-B (Supplemental) Approval Date',
    'Strategic Program', 'Project Cost (CEO Appr.)', 'IBRD PO ID',
    'GEF Agency Approval Date', 'GEF Agency Fees (CEO Appr.)',
    'Project Cost (CEO Endo.)']
    """
    data =  get_gef_iw_project_page()
    gefids = extract_gefids_from_page(data)
    info_keys = []
    countries = []
    #priorities = []
    project_statuses = []
    operational_programmes = []
    focal_areas = []
    strategic_programs = []

    for gefid in gefids:
        info = extract_project_info(gefid)
        info_keys += info.keys()
        countries += get_countries(info.get('Country', ''))
        project_statuses.append(info.get('Project Status', ''))
        operational_programmes.append(info.get('Operational Program', ''))
        focal_areas.append(info.get('Focal Area',''))
        strategic_programs.append(info.get('Strategic Program', ''))
    return [set(info_keys), set(countries),
        set(project_statuses), set(focal_areas), set(strategic_programs)]


GEF_COUNTRIES=[u'Afghanistan', u'Africa', u'Albania', u'Algeria', u'Angola', u'Antigua And Barbuda', u'Argentina', u'Armenia', u'Asia/Pacific', u'Azerbaijan', u'Bahamas', u'Bangladesh', u'Barbados', u'Belarus', u'Belize', u'Benin', u'Bolivia', u'Bosnia-Herzegovina', u'Botswana', u'Brazil', u'Bulgaria', u'Burkina Faso', u'Burundi', u'Cambodia', u'Cameroon', u'Cape Verde', u'Central African Republic', u'Chad', u'Chile', u'China', u'Colombia', u'Comoros', u'Congo', u'Congo DR', u'Cook Islands', u'Costa Rica', u"Cote d'Ivoire", u'Croatia', u'Cuba', u'Czech Republic', u'Djibouti', u'Dominica', u'Dominican Republic', u'Ecuador', u'Egypt', u'El Salvador', u'Equatorial Guinea', u'Eritrea', u'Estonia', u'Ethiopia', u'Fiji', u'Gabon', u'Gambia', u'Georgia', u'Ghana', u'Global', u'Grenada', u'Guatemala', u'Guinea', u'Guinea-Bissau', u'Guyana', u'Haiti', u'Honduras', u'Hungary', u'India', u'Indonesia', u'Iran', u'Jamaica', u'Jordan', u'Kazakhstan', u'Kenya', u'Kiribati', u'Korea DPR', u'Kyrgyzstan', u'Lao PDR', u'Latin America and Caribbean', u'Latvia', u'Lebanon', u'Lesotho', u'Liberia', u'Libya', u'Lithuania', u'Macedonia', u'Madagascar', u'Malaysia', u'Maldives', u'Mali', u'Marshall Islands', u'Mauritania', u'Mauritius', u'Mexico', u'Micronesia', u'Moldova', u'Mongolia', u'Montenegro', u'Morocco', u'Mozambique', u'Namibia', u'Nauru', u'Nicaragua', u'Niger', u'Nigeria', u'Niue', u'Palau', u'Palestinian Authority', u'Panama', u'Papua New Guinea', u'Paraguay', u'Peru', u'Philippines', u'Poland', u'Republic Of Korea', u'Romania', u'Russian Federation', u'Rwanda', u'Samoa', u'Sao Tome and Principe', u'Saudi Arabia', u'Senegal', u'Serbia', u'Serbia and Montenegro', u'Seychelles', u'Sierra Leone', u'Slovak Republic', u'Slovenia', u'Solomon Islands', u'South Africa', u'Sri Lanka', u'St. Kitts And Nevis', u'St. Lucia', u'St. Vincent and Grenadines', u'Sudan', u'Suriname', u'Syria', u'Tajikistan', u'Tanzania', u'Thailand', u'Timor Leste', u'Togo', u'Tokelau', u'Tonga', u'Trinidad and Tobago', u'Tunisia', u'Turkey', u'Turkmenistan', u'Tuvalu', u'Uganda', u'Ukraine', u'Uruguay', u'Uzbekistan', u'Vanuatu', u'Venezuela', u'Vietnam', u'Yemen', u'Zambia', u'Zimbabwe']

def compare_countries():

    plone_countries = [c['name'] for c in _countrylist.values()]
    for c in GEF_COUNTRIES:
        if c in plone_countries:
            continue
        else:
            print c
