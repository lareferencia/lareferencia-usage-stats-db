from lareferenciastatsdb.models import Source
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, select
from config import read_ini


config = read_ini("config.ini")
database_connection_str = config["DB"]["SQLALCHEMY_DATABASE_URI"] 
matomo_connection_str = config["MATOMO"]["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(database_connection_str)
connection = engine.connect()
metadata = MetaData()

engine_matomo = create_engine(matomo_connection_str)
connection_matomo = engine_matomo.connect()

# Asume que 'engine' es tu objeto de conexión SQLAlchemy ya creado
with Session(engine) as session:
    sources = session.query(Source).all()
    for source in sources:

        query = """select idsite, SUBSTRING(custom_var_v1, 1, LOCATE(":", custom_var_v1, 12)-1) as identifier_prefix
                from matomo.matomo_log_link_visit_action va
                where idsite = %s and server_time >= '2022-01-01' 
                limit 1""" % (source.site_id)
        
        result = connection_matomo.execute(query)
        
        # Get the first row
        row = result.fetchone()

        if row is not None and row[1] is not None and row[1] != "":
            print(source.source_id, source.site_id,  row[1])
        
