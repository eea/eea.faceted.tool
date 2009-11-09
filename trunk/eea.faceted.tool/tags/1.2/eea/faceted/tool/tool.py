from eea.faceted.tool.interfaces import IFacetedTool
from eea.faceted.tool.interfaces import IFacetedCatalog

from zope.interface import implements
from OFS.Folder import Folder
from Products.CMFCore.utils import getToolByName
from zope.app import zapi

class FacetedTool(Folder):
    """ A local utility storing all faceted navigation global settings """
    implements(IFacetedTool)

    id  = 'portal_faceted'
    title = 'Manages faceted navigation global settings'
    meta_type = 'EEA Faceted Tool'

    def search(self, **query):
        """
        Use this method to search over catalog using defined
        faceted portal types.
        """
        ctool = getToolByName(self, 'portal_catalog')
        catalog = zapi.queryMultiAdapter((self, ctool), IFacetedCatalog)
        if not catalog:
            return ctool(**query)
        return catalog(**query)
