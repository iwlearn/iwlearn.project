from zope.interface import implements
from zope.interface import Interface
from z3c.form import form, field, button
from zope import schema
from plone.z3cform.layout import wrap_form
from collective.z3cform.colorpicker.colorpickeralpha import ColorpickerAlphaFieldWidget


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
    country_fill = 'ff0000cc'
    country_border = 'ff0000cc'

    oo_fill = 'ff0000cc'
    oo_border = 'ff0000cc'

    lme_fill = 'ff0000cc'
    lme_border = 'ff0000cc'

    lake_fill = 'ff0000cc'
    lake_border = 'ff0000cc'

    river_fill = 'ff0000cc'
    river_border = 'ff0000cc'

    gw_fill = 'ff0000cc'
    gw_border = 'ff0000cc'

    def __init__(self, context):
        self.context = context


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

    def applyChanges(self, data):
        pass

    @button.buttonAndHandler(u'Save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return
        else:
            import ipdb; ipdb.set_trace()
        return

UpdateColors = wrap_form(ColorUpdateForm)
