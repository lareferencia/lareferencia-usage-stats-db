from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from .normalize import normalize_oai_identifier_prefix, extract_oai_identifier_prefix
from .models import Source, SOURCE_TYPE_REPOSITORY, SOURCE_TYPE_NATIONAL, SOURCE_TYPE_REGIONAL

class IdentifierPrefixNotFoundException(Exception):
    pass

"""
Get a Source object from the database by source_id
"""
def get_source_by_id(database_uri, source_id):

    engine = create_engine(database_uri)
    with Session(engine) as session:
        return session.query(Source).filter(Source.source_id == source_id).first()

"""
Get a Source object from the database by site_id
"""
def get_source_by_site_id(database_uri, site_id):
        engine = create_engine(database_uri)
        with Session(engine) as session:
            return session.query(Source).filter(Source.site_id == site_id).first()


""""
Get and store the sources data from the database and create the dicts for fast access to the data
"""
class UsageStatsDatabaseHelper:

    DEFAULT_REGIONAL_SITE_ID = 1

    def __init__(self, config):
        self.config = config
        self.engine = create_engine(config["USAGE_STATS_DB"]["SQLALCHEMY_DATABASE_URI"])

        # create dicts to store data
        self.sources_by_id = {}
        self.sources_by_site_id = {}
        self.sources_by_identifer_prefix = {}
        self.national_sources_by_country_iso = {}
        self.repository_sources_by_country_iso = {}
        self.country_by_identifier_prefix = {}

        self.update_data_from_db()

    """
    Update the data from the database
    """
    def update_data_from_db(self):

        # iterate over the sources and store the data in the dicts
        with Session(self.engine) as session:

            sources = session.query(Source).all()
            for source in sources:

                # normalize the source_id to lowercase
                source_id = source.source_id.lower()    

                # store the source data in the dicts
                self.sources_by_id[source_id] = source
                self.sources_by_site_id[source.site_id] = source

                if source.type == SOURCE_TYPE_REPOSITORY and source.identifier_prefix is not None:
                    normalized_oai_prefix = normalize_oai_identifier_prefix(source.identifier_prefix)
                    if normalized_oai_prefix is not None:
                        self.sources_by_identifer_prefix[normalized_oai_prefix] = source
                        self.country_by_identifier_prefix[normalized_oai_prefix] = source.country_iso

                if source.type == SOURCE_TYPE_REPOSITORY and source.country_iso is not None and source.country_iso != "":
                    repositories = self.repository_sources_by_country_iso.get(source.country_iso.lower(), [])
                    repositories.append(source)
                    self.repository_sources_by_country_iso[source.country_iso.lower()] = repositories

                if source.type == SOURCE_TYPE_NATIONAL and source.country_iso is not None and source.country_iso != "":
                    self.national_sources_by_country_iso[source.country_iso.lower()] = source


    """
    Get the identifier prefix from the source_id
    """
    def get_identifier_prefix_from_source(self, source):
        
        if source is None:
            raise Exception("Source %s not found in the database " % str(source))

        return normalize_oai_identifier_prefix(source.identifier_prefix)
        

    """
    Get source data by source_id
    """
    def get_source_by_id(self, source_id):
        return self.sources_by_id.get(source_id.lower(), None)
    
    """
    Get source data by site_id
    """
    def get_source_by_site_id(self, site_id):
        return self.sources_by_site_id.get(site_id, None)
    
    """
    Get source data by identifier prefix
    """ 
    def get_source_by_identifier_prefix(self, identifier_prefix):
        return self.sources_by_identifer_prefix.get(identifier_prefix, None)
    
    """"
    Get source data by country_iso
    """
    def get_source_by_country_iso(self, country_iso):
        return self.national_sources_by_country_iso.get(country_iso, None)
    

    """
    Get all sources site_ids
    """
    def get_all_site_ids(self):
        return self.sources_by_site_id.keys()
    
    """
    Get all national sources
    """
    def get_national_sources(self):
        return [source for source in self.national_sources_by_country_iso.values()]    
    
    """
    Get all repository sources by country_iso
    """
    def get_repository_sources_by_country_iso(self, country_iso):
        return self.repository_sources_by_country_iso.get(country_iso, [])
    

    """
    Get the site_id, national_site_id and regional_site_id from identifier
    :param identifier: the identifier of the item
    :return: list with indices names
    :raise Exception: if the identifier prefix is not found in the database
    """                
    def get_indices_from_identifier(self, index_prefix, identifier):

        index_names = []

        if identifier is None or identifier == "":
            raise Exception(status_code=400, detail="Identifier parameter is required")
        
        normalized_oai_prefix = extract_oai_identifier_prefix(identifier)
        #print(normalized_oai_prefix)
     
        identifier_source = self.get_source_by_identifier_prefix(normalized_oai_prefix)
        if identifier_source is None:
            raise IdentifierPrefixNotFoundException("Identifier prefix not found in the database")

        site_id = identifier_source.site_id
        national_site_id = identifier_source.national_site_id
        regional_site_id = identifier_source.regional_site_id

        if regional_site_id is None:
            regional_site_id = self.DEFAULT_REGIONAL_SITE_ID

        index_names.append(self.get_index_name(index_prefix,site_id))
        index_names.append(self.get_index_name(index_prefix,national_site_id))
        index_names.append(self.get_index_name(index_prefix,regional_site_id))

        return index_names
    
    """
    Get indices from source
    :param source: the source to search for
    :return: list with indices names
    :raise Exception: if the source_id is not found in the database
    """             
    def get_indices_from_source(self, index_prefix, source):

        index_names = set()

        if source.type == SOURCE_TYPE_REPOSITORY:
            site_id = source.site_id
            national_site_id = source.national_site_id
            regional_site_id = source.regional_site_id

        elif source.type == SOURCE_TYPE_NATIONAL:
            site_id = None
            national_site_id = source.site_id
            regional_site_id = source.regional_site_id

        elif source.type == SOURCE_TYPE_REGIONAL:
            site_id = None
            national_site_id = None
            regional_site_id = source.site_id
            
            for national_source in self.get_national_sources():
                index_names.add(self.get_index_name(index_prefix,national_source.site_id))

        if site_id is not None:
            index_names.add(self.get_index_name(index_prefix,site_id))

        if national_site_id is not None:
            index_names.add(self.get_index_name(index_prefix,national_site_id))

        if regional_site_id is None:
            regional_site_id = self.DEFAULT_REGIONAL_SITE_ID
        index_names.add(self.get_index_name(index_prefix,regional_site_id))

        return list(index_names)
    
    """
    Get indices for the national source and all repositories of that country
    :param source: the source to search for
    :return: list with indices names
    :raise Exception: if the source_id is not found in the database
    """             
    def get_indices_from_national_source(self, index_prefix, source):

        index_names = set()

        if source is None or source.type != SOURCE_TYPE_NATIONAL:
            raise Exception("Source %s not found in the database " % source)

        index_names.add(self.get_index_name(index_prefix,source.site_id))

        for repository in self.get_repository_sources_by_country_iso(source.country_iso.lower()):
            index_names.add(self.get_index_name(index_prefix,repository.site_id))

        index_names.add(self.get_index_name(index_prefix,self.DEFAULT_REGIONAL_SITE_ID))

        return list(index_names)
    

    """
    Get indices for the national source and all repositories of that country
    :param source: the source to search for
    :return: list with indices names
    :raise Exception: if the source_id is not found in the database
    """             
    def get_indices_from_regional_source(self, index_prefix, source):

        index_names = set()

        if source is None or source.type != SOURCE_TYPE_REGIONAL:
            raise Exception("Source %s not found in the database " % source)

        index_names.add(self.get_index_name(index_prefix,'*'))

        return list(index_names)
    

    def get_index_name(self, index_prefix, idsite):
        return '%s-%s' % (index_prefix, idsite)
    
   
    