from zope.interface import implements
from zope.interface import Interface
from z3c.form import form, field, button
from zope import schema
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from collective.z3cform.colorpicker.colorpickeralpha import ColorpickerAlphaFieldWidget
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle


class IColorForm(Interface):
    country_fill = schema.TextLine(title=u"Country Fillcolor",
                               description=u"",
                               required=True)

    country_border = schema.TextLine(title=u"Country Outline Color",
                               description=u"",
                               required=True)


    oo_fill = schema.TextLine(title=u"Oceans Fillcolor",
                               description=u"",
                               required=True)

    oo_border = schema.TextLine(title=u"Oceans Outline Color",
                               description=u"",
                               required=True)

    lme_fill = schema.TextLine(title=u"LME Fillcolor",
                               description=u"",
                               required=True)

    lme_border = schema.TextLine(title=u"LME Outline Color",
                               description=u"",
                               required=True)

    lake_fill = schema.TextLine(title=u"Lake Fillcolor",
                               description=u"",
                               required=True)

    lake_border = schema.TextLine(title=u"Lake Outline Color",
                               description=u"",
                               required=True)

    river_fill = schema.TextLine(title=u"River Fillcolor",
                               description=u"",
                               required=True)

    river_border = schema.TextLine(title=u"River Outline Color",
                               description=u"",
                               required=True)

    gw_fill = schema.TextLine(title=u"Aquifer Fillcolor",
                               description=u"",
                               required=True)

    gw_border = schema.TextLine(title=u"Aquifer Outline Color",
                               description=u"",
                               required=True)

class Color(object):
    implements(IColorForm)
    #country_fill = '7fff00cc'
    #country_border = 'ff0000cc'

    #oo_fill = 'ff0000cc'
    #oo_border = 'ff0000cc'

    #lme_fill = '0000bfcc'
    #lme_border = 'ff0000cc'

    #lake_fill = '2c80d3cc'
    #lake_border = 'ff0000cc'

    #river_fill = '56ffffcc'
    #river_border = 'ff0000cc'

    #gw_fill = 'c1742ccc'
    #gw_border = 'ff0000cc'
    COLORS = ['gw_border', 'river_fill', 'lme_fill', 'country_border',
        'lake_border', 'gw_fill', 'lake_fill', 'oo_border', 'lme_border',
        'oo_fill', 'country_fill', 'river_border']

    def __init__(self, context):
        self.context = context
        for c in self.COLORS:
            setattr(self, c, getattr(self.context, c))


class ColorUpdateForm(form.Form):
    """Example color picker form"""

    fields = field.Fields(IColorForm)

    fields['country_fill'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['country_border'].widgetFactory = ColorpickerAlphaFieldWidget

    fields['oo_fill'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['oo_border'].widgetFactory = ColorpickerAlphaFieldWidget

    fields['lme_fill'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['lme_border'].widgetFactory = ColorpickerAlphaFieldWidget

    fields['lake_fill'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['lake_border'].widgetFactory = ColorpickerAlphaFieldWidget

    fields['river_fill'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['river_border'].widgetFactory = ColorpickerAlphaFieldWidget

    fields['gw_fill'].widgetFactory = ColorpickerAlphaFieldWidget
    fields['gw_border'].widgetFactory = ColorpickerAlphaFieldWidget

    def __init__(self, context, request):
        super(ColorUpdateForm, self).__init__(context, request)
        self.request.set('disable_border', True)

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def _set_color(self, query, fc, bc):
        brains = self.portal_catalog(**query)
        for brain in brains:
            ob = brain.getObject()
            style = IGeoCustomFeatureStyle(ob)
            style.geostyles.data['polygoncolor']=fc
            style.geostyles.data['linecolor']=bc
            style.geostyles.data['use_custom_styles']=True
            style.geostyles.update(style.geostyles)
            ob.reindexObject()

    def set_colors(self):
        query = {'portal_type': 'Basin', 'getBasin_type': 'Ocean'}
        bc = self.context.getOo_border()
        fc = self.context.getOo_fill()
        self._set_color(query, fc, bc)

        query = {'portal_type': 'Basin', 'getBasin_type': 'LME'}
        bc = self.context.getLme_border()
        fc = self.context.getLme_fill()
        self._set_color(query, fc, bc)

        query = {'portal_type': 'Basin', 'getBasin_type': 'River'}
        bc = self.context.getRiver_border()
        fc = self.context.getRiver_fill()
        self._set_color(query, fc, bc)

        query = {'portal_type': 'Basin', 'getBasin_type': 'Lake'}
        bc = self.context.getLake_border()
        fc = self.context.getLake_fill()
        self._set_color(query, fc, bc)

        query = {'portal_type': 'Basin', 'getBasin_type': 'Aquifer'}
        bc = self.context.getGw_border()
        fc = self.context.getGw_fill()
        self._set_color(query, fc, bc)

        query = {'portal_type': 'Image', 'path': 'iwlearn/images/countries/'}
        bc = self.context.getCountry_border()
        fc = self.context.getCountry_fill()
        self._set_color(query, fc, bc)


    @button.buttonAndHandler(u'Save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return
        else:
            for k, v in data.iteritems():
                if getattr(self.context, k) != v:
                    setattr(self.context, k, v)
            self.set_colors()
        return

UpdateColors = wrap_form(ColorUpdateForm)
