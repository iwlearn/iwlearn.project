#
import csv

def map_rating(ra):
    r = ra.strip()
    if r.lower() == 'n/a':
        return -1
    elif r == '':
        return None
    else:
        return int(r)


def import_ra(self):
    data = csv.DictReader(open(
        'src/iwlearn.project/iwlearn/project/dataimport/ra.csv', 'r'))
    raid = {}
    for d in data:
        raid[d['GEFID']] = {
            'csim_committees': map_rating(d['Establishment of country-specific inter-ministerial committees']),
            'regional_frameworks': map_rating(d['Regional legal agreements and cooperation frameworks']),
            'rmis': map_rating(d['Regional Management Institutions']),
            'reforms': map_rating(d['National/Local reforms']),
            'tda_priorities': map_rating(d['Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes']),
            'sap_devel': map_rating(d['Development of Strategic Action Plan (SAP)']),
        }
    for brain in self.portal_catalog(portal_type = 'Project'):
        if brain.getId in raid:
            ob = brain.getObject()
            ob.update(**raid[brain.getId])

if __name__ == '__main__':
    import_ra(None)

