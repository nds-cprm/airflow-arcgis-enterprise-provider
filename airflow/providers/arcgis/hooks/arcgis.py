# from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from arcgis.gis import GIS
from bs4 import BeautifulSoup
from typing import Any, cast
from urllib.parse import urlparse


class ArcGISHook(BaseHook):
    """
    """
    conn_name_attr = "arcgis_conn_id"
    default_conn_name = "arcgis_default"
    conn_type = "arcgis"
    hook_name = "ArcGIS Online/Enterprise"

    def __init__(self, arcgis_conn_id=default_conn_name):
        super().__init__()
        self.arcgis_conn_id=arcgis_conn_id
        self.portal_url = ''
    
    def get_conn(self) -> Any:
        """
        """
        conn_id = getattr(self, cast(str, self.conn_name_attr))
        kwargs = {}

        if conn_id:
            conn = self.get_connection(conn_id)            

            if conn.host and "://" in conn.host:
                self.portal_url = conn.host

            else:
                schema = conn.schema if conn.schema else "https"
                host = conn.host if conn.host else ""

                self.portal_url = schema + "://" + host
            
            # Parse URL to check and add some completions
            result = urlparse(self.portal_url)
            assert all([result.scheme, result.netloc])

            # Add port
            if conn.port:
                print("port: %s", conn.port)
                result = result._replace(netloc=result.netloc + ":" + str(conn.port))

            # Check webadaptor and other stuff
            if conn.extra:
                kwargs = conn.extra_dejson

                # Add webadaptor
                webadaptor = kwargs.get("webadaptor")                

                if webadaptor and result.path in ("", "/"):
                    result = result._replace(path=webadaptor)

                # remove redundant parameters
                for key in ['url', 'username', 'password']:
                    if key in kwargs:
                        self.log.warn("Ignoring key '%s', passed as 'Extra' field", key)
                        del kwargs[key]
            
            # dump portal URL
            self.portal_url = result.geturl()

        if self.portal_url:
            kwargs.update({'url': self.portal_url})
        
        return GIS(username=conn.login, password=conn.get_password(), **kwargs)

    def run(self):
        gis = self.get_conn()
        return gis

    def test_connection(self):
        """Test HTTP Connection"""
        try:
            self.run()
            return True, f"Connected to ArcGIS Portal/Enterprise: {self.portal_url}"

        except Exception as e:
            error_class = e.__class__.__name__
            message = BeautifulSoup(str(e), 'html.parser').get_text()

            return False, f"Failed to check URL {self.portal_url}: [{error_class}]: {message}"
