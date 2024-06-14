import unittest

from lareferenciastatsdb import UsageStatsDatabaseHelper, get_source_by_id


import configparser

def read_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    #for section in config.sections():
    #    for key in config[section]:
    #        print((key, config[section][key]))
    
    return config

class TestSimple(unittest.TestCase):

    def test_add(self):
         
        config = read_ini("config.tst.ini")

        helper = UsageStatsDatabaseHelper(config)

        print( helper.get_source_by_id("SITEID::1") )
        print( helper.get_source_by_site_id(1) )
        print( helper.get_source_by_country_iso("AR") )

        #print( helper.get_indices_from_identifier("oai:repositorio.ucv.edu.pe:20.500.12692/32743") )
        
    def test_get_indices_by_source(self):
         
        config = read_ini("config.tst.ini")

        helper = UsageStatsDatabaseHelper(config)

        print( helper.get_indices_from_source("SITEID::1") )
        print( helper.get_indices_from_source("SITEID::59") )
        print( helper.get_indices_from_source("OPENDOAR::1329") )

    def test_get_source_by_source_id(self):
        config = read_ini("config.tst.ini")
        print ( get_source_by_id(config, "SITEID::1").name )




              
        







if __name__ == '__main__':
    unittest.main()
