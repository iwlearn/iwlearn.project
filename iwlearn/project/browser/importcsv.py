from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from iwlearn.project import projectMessageFactory as _

class IImportCSVSchema(interface.Interface):
    # -*- extra stuff goes here -*-

    csvupload = schema.Bytes(
        title=_(u'CSV File'),
        description=_(u'CSV File to be uploaded'),
        required=True,
        readonly=False,
        default=None,
        )


class ImportCSV(formbase.PageForm):
    form_fields = form.FormFields(IImportCSVSchema)
    label = _(u'Import CSV')
    description = _(u'''Import a CSV file to add new projects to the
    Project DB and to update existing projects with data from the CSV''')

    @form.action('Submit')
    def actionSubmit(self, action, data):
        pass
        # Put the action handler code here



