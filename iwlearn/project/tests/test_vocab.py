# test vocabularies
import unittest
from iwlearn.project import vocabulary


class SubregionTestCase( unittest.TestCase ):
    """ Test the subregions"""
    def test_all_subregions(self):
        result = vocabulary.get_subregions()
        self.assertEqual(result, [u'Central Africa', u'Eastern Africa',
            u'Indian Ocean', u'Northern Africa', u'Southern Africa',
            u'Western Africa', u'Caribbean', u'Central America',
            u'North America', u'South America', u'Antarctica',
            u'Central Asia', u'East Asia', u'Northern Asia',
            u'South Asia', u'South East Asia', u'South West Asia',
            u'South Atlantic Ocean', u'Central Europe', u'Eastern Europe',
            u'Northern Europe', u'South East Europe', u'South West Europe',
            u'Southern Europe', u'Western Europe', u'Southern Indian Ocean',
            u'Australasia', u'Melanesia', u'Micronesia', u'Polynesia'])

    def test_regions(self):
        result = vocabulary.get_subregions(regions=['Africa'])
        self.assertEqual(result, [u'Central Africa', u'Eastern Africa',
            u'Indian Ocean', u'Northern Africa', u'Southern Africa',
            u'Western Africa'])

        result = vocabulary.get_subregions(regions=['Africa', 'Europe'])
        self.assertEqual(result,[u'Central Africa', u'Eastern Africa',
            u'Indian Ocean', u'Northern Africa', u'Southern Africa',
            u'Western Africa', u'Central Europe', u'Eastern Europe',
            u'Northern Europe', u'South East Europe', u'South West Europe',
            u'Southern Europe', u'Western Europe'])

        result = vocabulary.get_subregions(regions=['Global'])
        self.assertEqual(result,[])

    def test_subregions(self):
        result = vocabulary.get_subregions(subregions=['Polynesia'])
        self.assertEqual(result,[u'Polynesia'])

        result = vocabulary.get_subregions(subregions=['Polynesia','East Asia'])
        self.assertEqual(result,['East Asia', 'Polynesia'])

        result = vocabulary.get_subregions(subregions=['Global'])
        self.assertEqual(result,[])

    def test_countries(self):
        result =  vocabulary.get_subregions(countries=['Anguilla', 'Andorra', 'India'])
        self.assertEqual(result, [u'Caribbean', u'South Asia', u'South West Europe'] )

        result =  vocabulary.get_subregions(countries=['Egypt'])
        self.assertEqual(result, [u'Northern Africa', u'South West Asia'])

        result =  vocabulary.get_subregions(countries=['Kazakhstan'])
        self.assertEqual(result, [u'Central Asia', u'Eastern Europe'] )

        result =  vocabulary.get_subregions(countries=['Egypt', 'Kazakhstan'])
        self.assertEqual(result, [u'Northern Africa', u'Central Asia',
            u'South West Asia', u'Eastern Europe'])

    def test_combinations(self):
        result = vocabulary.get_subregions(subregions=['Polynesia'],
            regions=['Africa'])
        self.assertEqual(result,  [u'Central Africa', u'Eastern Africa',
            u'Indian Ocean', u'Northern Africa', u'Southern Africa',
            u'Western Africa', u'Polynesia'])
        result = vocabulary.get_subregions(subregions=['Polynesia','East Asia'] ,
            countries=['Egypt', 'Kazakhstan'])
        self.assertEqual(result,[u'Northern Africa', u'Central Asia', 'East Asia',
            u'South West Asia', u'Eastern Europe', 'Polynesia'])
        result = vocabulary.get_subregions(subregions=['Polynesia','East Asia'] ,
            regions=[u'Atlantic Ocean'])
        self.assertEqual(result, ['East Asia', u'South Atlantic Ocean', 'Polynesia'])
        result = vocabulary.get_subregions(countries=['Egypt', 'Kazakhstan'],
            regions=[u'Antarctica'])
        self.assertEqual(result, [u'Northern Africa', u'Antarctica',
            u'Central Asia', u'South West Asia', u'Eastern Europe'])



class CountryTestCase( unittest.TestCase ):
    """ Test the countries"""

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

    def test_combinations(self):
        result = vocabulary.get_regions(subregions=['Polynesia'],
            regions=['Africa'])
        self.assertEqual(result, [u'Africa', u'Oceania'])
        result = vocabulary.get_regions(subregions=['Polynesia','East Asia'] ,
            countries=['Egypt', 'Kazakhstan'])
        self.assertEqual(result,[u'Africa', u'Asia', u'Europe', u'Oceania'] )
        result = vocabulary.get_regions(subregions=['Polynesia','East Asia'] ,
            regions=[u'Global'])
        self.assertEqual(result, [u'Asia', u'Global', u'Oceania'])
        result = vocabulary.get_regions(countries=['Egypt', 'Kazakhstan'],
            regions=[u'Global'])
        self.assertEqual(result, [u'Africa', u'Asia', u'Europe', u'Global'])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite( RegionTestCase ))
    suite.addTest(unittest.makeSuite( SubregionTestCase ))
    suite.addTest(unittest.makeSuite( CountryTestCase ))

    return suite

if __name__ == '__main__':
    unittest.main()
