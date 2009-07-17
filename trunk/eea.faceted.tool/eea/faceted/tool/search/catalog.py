import logging
from zope.interface import implements
from types import StringTypes, TupleType, ListType, DictType
from interfaces import IFacetedCatalog

logger = logging.getLogger('eea.faceted.tool.search')
ListTypes = (TupleType, ListType)

class FacetedCatalog(object):
    """ Adapts portal_catalog to be used together with portal_faceted tool.
    """
    implements(IFacetedCatalog)

    def __init__(self, context, catalog):
        self.context = context
        self.catalog = catalog

    @property
    def faceted_types(self):
        """ Get custom portal types defined by faceted tool
        """
        return self.context.objectIds('EEA Faceted Portal Type')

    def _index2dict(self, index):
        """ Convert index to search dict
        """
        if isinstance(index, StringTypes):
            return {'query': [index], 'operator': 'or'}
        if isinstance(index, ListTypes):
            return {'query': list(index), 'operator': 'or'}
        if isinstance(index, DictType):
            index.setdefault('operator', 'or')
            query = index.get('query', [])
            query = self._index2list(query)
            index['query'] = query
            return index

        logger.warn('Unknown index type: %s', index)
        return {'query': [], 'operator': 'or'}

    def _index2list(self, index):
        """ Convert index to list
        """
        if not index:
            return []
        if isinstance(index, StringTypes):
            return [index]
        if isinstance(index, TupleType):
            return list(index)
        if isinstance(index, DictType):
            return index.keys()
        return index

    def __call__(self, **query):
        portal_types = query.pop('portal_type', [])
        if not portal_types:
            return self.catalog(**query)

        portal_types = self._index2dict(portal_types)
        pt_query = portal_types.get('query', [])
        common = [pt for pt in pt_query if pt in self.faceted_types]
        if not common:
            return self.catalog(portal_type=portal_types, **query)

        pt_query = portal_types['query'] = [pt for pt in pt_query
                                            if pt not in common]

        object_provides = query.pop('object_provides', [])
        object_provides = self._index2dict(object_provides)
        op_query = object_provides['query']

        for pt_id in common:
            faceted = self.context._getOb(pt_id)

            faceted_search_type = getattr(faceted, 'search_type', '')
            if faceted_search_type and faceted_search_type not in pt_query:
                pt_query.append(faceted_search_type)

            faceted_search_interface = getattr(faceted, 'search_interface', '')
            if faceted_search_interface and faceted_search_interface not in op_query:
                op_query.append(faceted_search_interface)

        return self.catalog(
            object_provides=object_provides,
            portal_type=portal_types, **query)
