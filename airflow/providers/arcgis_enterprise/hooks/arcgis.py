from airflow.hooks.base import BaseHook
from arcgis.gis import GIS
from bs4 import BeautifulSoup
from typing import cast, Tuple
from urllib.parse import urlparse


class ArcGISHook(BaseHook):
    """
    """
    conn_name_attr: str = "arcgis_conn_id"
    default_conn_name: str = "arcgis_default"
    conn_type: str = "arcgis"
    hook_name: str = "ArcGIS Online/Enterprise"

    def __init__(self, arcgis_conn_id: str = default_conn_name):
        super().__init__()
        self.arcgis_conn_id=arcgis_conn_id
        self.portal_url = ''
        # self._gis = self.get_conn()


    def get_uri(self) -> str:
        """
        Extract the URI from the connection.
        :return: the extracted uri.
        """
        conn_id = getattr(self, cast(str, self.conn_name_attr))
        url = None

        if conn_id:
            conn = self.get_connection(conn_id)            

            if conn.host:
                if conn.host.startswith("http://") or conn.host.startswith("https://"):
                    url = conn.host
                else:
                    url = f"{conn.schema if conn.schema else "https"}://{conn.host}"                
            
                # Parse URL to check and add some completions
                result = urlparse(url)
                assert all([result.scheme, result.netloc])

                # Add port
                if conn.port:
                    result = result._replace(netloc=f"{result.netloc}:{str(conn.port)}")
                
                # dump ArcGIS Portal URL
                url = result.geturl()
        
        return url
        
    
    def get_conn(self) -> GIS:
        """
        Returns a ArcGIS GIS object
        :return: a instance of arcgis.gis.GIS object
        """
        conn_id = getattr(self, cast(str, self.conn_name_attr))
        
        # Adiciona URI do portal
        kwargs = {'url': self.get_uri()}

        # Check extra params
        # https://developers.arcgis.com/python/latest/api-reference/arcgis.gis.toc.html#gis
        if conn_id:
            conn = self.get_connection(conn_id)
            
            if conn.extra:
                kwargs = conn.extra_dejson

                # remove redundant parameters
                for key in ['url', 'username', 'password']:
                    if key in kwargs:
                        self.log.warning("Ignoring key '%s', passed as 'Extra' field", key)
                        del kwargs[key]            
        
        return GIS(username=conn.login, password=conn.get_password(), **kwargs)
    

    def test_connection(self) -> Tuple[bool, str]:
        """
        Test ArcGIS Connection
        """
        try:
            gis = self.get_conn()
            return True, f"Connected to ArcGIS Portal/Enterprise: {gis}"

        except Exception as e:    
            error_class = e.__class__.__name__
            message = BeautifulSoup(str(e), 'html.parser').get_text()

            return False, f"Connection to ArcGIS failed {self.portal_url}: [{error_class}]: {message}"
