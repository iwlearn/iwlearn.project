from zope import schema
from zope.interface import Interface

from iwlearn.project import projectMessageFactory as _


class IProject(Interface):
    """GEF IW Project"""

    # -*- schema definition goes here -*-
    longitude = schema.Float(
        title=_(u"Longitude of an marker on map"),
        required=False,
        description=_(u"Longitude of an marker on map"),
    )
#
    latitude = schema.Float(
        title=_(u"Latitude of an marker on map"),
        required=False,
        description=_(u"Latitude of an marker on map"),
    )
#
    evaluator_name = schema.TextLine(
        title=_(u"Name of Evaluator"),
        required=False,
        description=_(u"Field description"),
    )
#
    terminal_evaluation_date = schema.Date(
        title=_(u"Terminal Evaluation Date"),
        required=False,
        description=_(u"Terminal Evaluation Date"),
    )
#
    consultant_name = schema.TextLine(
        title=_(u"Name of Consultant"),
        required=False,
        description=_(u"Name of Consultant"),
    )
#
    evaluation_report_date = schema.Date(
        title=_(u"Evaluation Report Date"),
        required=False,
        description=_(u"Evaluation Report Date"),
    )
#
    project_results = schema.SourceText(
        title=_(u"Project Results"),
        required=False,
        description=_(u"Project Results"),
    )
#
    total_cost = schema.Float(
        title=_(u"Total Cost"),
        required=False,
        description=_(u"Total Cost"),
    )
#
    gef_project_allocation = schema.Float(
        title=_(u"GEF Allocation to project"),
        required=False,
        description=_(u"GEF Allocation to project"),
    )
#
    gef_project_stage = schema.TextLine(
        title=_(u"New Field"),
        required=False,
        description=_(u"GEF Project Stage"),
    )
#
    project_type = schema.TextLine(
        title=_(u"Project Type"),
        required=False,
        description=_(u"Project Type"),
    )
#
    gef_project_id = schema.TextLine(
        title=_(u"GEF Project Id"),
        required=False,
        description=_(u"GEF Project Id"),
    )
#
    focal_area = schema.TextLine(
        title=_(u"Focal Areas"),
        required=False,
        description=_(u"Focal Areas"),
    )
#
    operational_programme = schema.List(
        title=_(u"GEF Operational Programme"),
        required=False,
        description=_(u"GEF Operational Programme"),
    )
#
    strategic_priority = schema.List(
        title=_(u"GEF Strategic Priority"),
        required=False,
        description=_(u"GEF Strategic Priority"),
    )
#
    project_summary = schema.SourceText(
        title=_(u"Project Description"),
        required=False,
        description=_(u"Project Description"),
    )
#
    end_date = schema.Date(
        title=_(u"End date"),
        required=False,
        description=_(u"End date"),
    )
#
    start_date = schema.Date(
        title=_(u"Start Date"),
        required=False,
        description=_(u"Start Date"),
    )
#
    project_status = schema.TextLine(
        title=_(u"Project Status"),
        required=False,
        description=_(u"Project Status"),
    )
#
    other_partners = schema.List(
        title=_(u"Other Partners"),
        required=False,
        description=_(u"Other Partners"),
    )
#
    executing_agency = schema.List(
        title=_(u"Executing Agencies"),
        required=False,
        description=_(u"Executing Agencies"),
    )
#
    other_implementing_agency = schema.List(
        title=_(u"Other Implementing Agencies"),
        required=False,
        description=_(u"Other Implementing Agencies"),
    )
#
    leadagency = schema.TextLine(
        title=_(u"Lead Implementing Agency"),
        required=False,
        description=_(u"Lead Implementing Agency"),
    )
#
    country = schema.List(
        title=_(u"Countries"),
        required=False,
        description=_(u"Countries"),
    )
#
    basin = schema.List(
        title=_(u"Basin"),
        required=False,
        description=_(u"Field description"),
    )
#
    subregion = schema.List(
        title=_(u"Geographic Sub Region"),
        required=False,
        description=_(u"Geographic Sub Region in which the project operates"),
    )
#
    region = schema.List(
        title=_(u"Geographic Region"),
        required=True,
        description=_(u"Geographic Region in which the project operates"),
    )
#
    project_contacts = schema.Object(
        title=_(u"Project Contacts"),
        required=False,
        description=_(u"Select Project Contacts"),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    remote_url = schema.TextLine(
        title=_(u"Project Website"),
        required=False,
        description=_(u"Website of the project"),
    )
#
