from zope import schema
from zope.interface import Interface
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from Products.ATContentTypes.interface import IATTopic

class IPortalType(Interface):
    """ Custom portal type
    """
    title = schema.TextLine(
        title=u'Title',
        description=u'Friendly name',
        required=True
    )

    search_interface = schema.Choice(
        title=u'Provided interface',
        description=u'Interface to search for',
        vocabulary="eea.faceted.tool.vocabularies.ObjectProvides",
        required=True
    )

    search_type = schema.Choice(
        title=u'Portal type',
        description=u'Portal type to search for',
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        required=False
    )
