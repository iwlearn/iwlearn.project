#
from collections import OrderedDict
from lxml import etree
from plone.i18n.normalizer import IDNormalizer

templates = {}
allowed_tags = []
allowed_self_closing_tags = []
allowed_attributes = []
interwiki = {}
namespaces = {}

from smc.mw.tool import run_preprocessor, run_parser

def process(input):
    profile_data = OrderedDict()
    result = run_preprocessor(input, filename='.', profile_data=profile_data)
    result = run_parser(result, filename='.', start=None, profile_data=profile_data, trace=False)
    result = result.encode("UTF-8")
    #result = result.lstrip('<html><body>')
    #result = result.rstrip('</body></html>')
    return result

def to_html(node, elem):
    source = node.find(elem)
    if source is not None:
        return process(source.text)

def import_legal_frameworks(self):
    f = open('dataimport/governance-ExportRDF.xml', 'rb')
    tree = etree.parse(f)
    f.close()
    idn = IDNormalizer()
    #preprocessor = make_parser(templates)
    #parser = make_parser(allowed_tags, allowed_self_closing_tags, allowed_attributes, interwiki, namespaces)
    for lf in tree.findall('{http://semantic-mediawiki.org/swivt/1.0#}Subject'):
        title = lf.find('{http://www.w3.org/2000/01/rdf-schema#}label').text
        new_id = idn.normalize(title)
        print title, new_id
        wt = lf.findall('{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Has_water_type')
        water_types = []
        if wt:
            for w in wt:
                for v in w.values():
                    water_types.append(v[56:].replace('_', ' '))
        notifications = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Notifications')
        organizational_structure = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Organizational_structure')
        participation_and_stakeholders = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Participation_and_stakeholders')
        references_urls = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}References')
        relationships = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Relationships')
        additional_remarks = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Additional_remarks')
        benefit_sharing = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Benefit_sharing')
        compliance_and_monitoring = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Compliance_and_monitoring')
        decision_making = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Decision_making')
        dispute_resolution = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Dispute_resolution')
        dissolution_and_termination = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Dissolution_and_termination')
        functions = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Functions')
        funding = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Funding_and_financing')
        geographical_scope = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Geographical_scope')
        information_sharing = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Information_sharing')
        legal_basis = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Legal_basis')
        legal_personality = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Legal_personality')
        member_states = to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Member_states')
        parent = self.portal_url.getPortalObject()['iw-projects']['legal-frameworks']
        self.portal_types.constructContent('LegalFW', parent, new_id)
        new_obj=parent[new_obj_id]
        new_obj.update(
            basin_type = ''.join(water_types),
            legal_basis = legal_basis,
            member_states = member_states,
            geographical_scope = geographical_scope,
            legal_personality = legal_personality,
            functions = functions,
            organizational_structure = organizational_structure,
            relationships = relationships,
            decision_making = decision_making,
            dispute_resolution = dispute_resolution,
            information_sharing = information_sharing,
            notifications = notifications,
            funding = funding,
            benefit_sharing = benefit_sharing,
            compliance_and_monitoring = compliance_and_monitoring,
            participation_and_stakeholders = participation_and_stakeholders,
            dissolution_and_termination = dissolution_and_termination,
            additional_remarks = additional_remarks,
            references_urls = references_urls)

    import ipdb; ipdb.set_trace()

import_legal_frameworks(None)

'{http://semantic-mediawiki.org/swivt/1.0#}Subject'

'{http://semantic-mediawiki.org/swivt/1.0#}page'
'{http://www.w3.org/2000/01/rdf-schema#}isDefinedBy'
'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}type'

'{http://semantic-mediawiki.org/swivt/1.0#}wikiNamespace'


#print to_html(lf,'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}Has_water_type'
'{http://localhost/watergov/index.php/Special:URIResolver/Property-3A}In_region'

'{http://semantic-mediawiki.org/swivt/1.0#}wikiPageModificationDate'

