import operator
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName

def compare(a, b):
    """ Compare lower values """
    return cmp(a.lower(), b.lower())

class FacetedPortalTypesVocabulary(object):
    """Vocabulary factory for faceted portal types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ptool = getToolByName(context, 'plone_utils', None)
        ttool = getToolByName(context, 'portal_types', None)
        ftool = getToolByName(context, 'portal_faceted', None)

        if ptool is None or ttool is None or ftool is None:
            return None

        items = dict((t, ttool[t].Title())
                     for t in ptool.getUserFriendlyTypes())
        faceted_items = dict((t.getId(), t.title_or_id())
                     for t in ftool.objectValues())
        items.update(faceted_items)
        items = items.items()
        items.sort(key=operator.itemgetter(1), cmp=compare)

        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

FacetedPortalTypesVocabularyFactory = FacetedPortalTypesVocabulary()
