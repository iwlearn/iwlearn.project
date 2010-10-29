# test vocabularies
import unittest
from iwlearn.project import vocabulary


class RegionTestCase( unittest.TestCase ):
    """ Test the regions"""

    def test_all_regions(self):
        result = vocabulary.get_regions()
        self.assertEqual(result, [u'Africa', u'Americas', u'Antarctica',
        u'Asia', u'Atlantic Ocean', u'Europe', u'Global',
        u'Indian Ocean', u'Oceania'])

    def test_regions(self):
        result = vocabulary.get_regions(regions=['Africa'])
        self.assertEqual(result, ['Africa'])

        result = vocabulary.get_regions(regions=['Africa', 'Europe'])
        self.assertEqual(result,['Africa', 'Europe'])

    def test_subregions(self):
        result = vocabulary.get_regions(subregions=['Polynesia'])
        self.assertEqual(result,[u'Oceania'])

        result = vocabulary.get_regions(subregions=['Polynesia','East Asia'])
        self.assertEqual(result,[u'Asia', u'Oceania'])

    def test_countries(self):
        result =  vocabulary.get_regions(countries=['Anguilla', 'Andorra', 'India'])
        self.assertEqual(result, [u'Americas', u'Asia', u'Europe'] )

        result =  vocabulary.get_regions(countries=['Egypt'])
        self.assertEqual(result, [u'Africa', u'Asia'] )

        result =  vocabulary.get_regions(countries=['Kazakhstan'])
        self.assertEqual(result, [u'Asia', u'Europe'] )

        result =  vocabulary.get_regions(countries=['Egypt', 'Kazakhstan'])
        self.assertEqual(result, [u'Africa', u'Asia', u'Europe'])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite( RegionTestCase ))
    return suite

if __name__ == '__main__':
    unittest.main()
