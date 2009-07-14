# Plone 2.5 compatible
from Products.CMFCore.utils import getToolByName

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-eea.faceted.tool.profiles:default')
    res = setup_tool.runAllImportSteps()
    messages = res.get('messages', {})
    output = [message for message in messages.values() if message]
    return '\n'.join(output)
