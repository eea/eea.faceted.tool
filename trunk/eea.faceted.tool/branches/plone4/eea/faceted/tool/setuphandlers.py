""" Various setup
"""

def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eeafacetedtool.txt') is None:
        return
