""" Base test cases
"""
import os
from StringIO import StringIO
from Globals import package_home
from cgi import FieldStorage
from ZPublisher.HTTPRequest import FileUpload
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from zope.app.component.hooks import setSite

product_globals = globals()

# Let Zope know about the two products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).

ztc.installProduct('Five')

# XXX Plone 2.x compatible
try: import Products.FiveSite
except ImportError: pass
else: ztc.installProduct('FiveSite')

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_eea_faceted_tool():
    """Set up the additional products.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)

    import eea.faceted.tool
    zcml.load_config('configure.zcml', eea.faceted.tool)
    fiveconfigure.debug_mode = False

EXTRA_PRODUCTS = []

setup_eea_faceted_tool()
setupPloneSite(
    products=EXTRA_PRODUCTS,
    extension_profiles=('eea.faceted.tool.profiles:default',)
)

class FacetedTestCase(PloneTestCase):
    """Base class for integration tests for the 'Faceted Tool' product.
    """
    def _setup(self):
        """ Setup test case
        """
        PloneTestCase._setup(self)
        # Set the local component registry
        setSite(self.portal)

class FacetedFunctionalTestCase(FunctionalTestCase, FacetedTestCase):
    """Base class for functional integration tests for the 'Faceted Tool' product.
    """
    def loadfile(self, rel_filename, ctype='text/xml'):
        """ load a file
        """
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = open(filename, 'r').read()

        fp = StringIO(data)
        fp.seek(0)

        header_filename = rel_filename.split('/')[-1]
        env = {'REQUEST_METHOD':'PUT'}
        headers = {'content-type' : ctype,
                   'content-length': len(data),
                   'content-disposition':'attachment; filename=%s' % header_filename}

        fs = FieldStorage(fp=fp, environ=env, headers=headers)
        return FileUpload(fs)
