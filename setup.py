import io
from os.path import dirname, join
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf-8")
    ).read()


setup(
    name="apache-airflow-providers-arcgis",
    version="1.0.0",
    description="ArcGIS Online/ArcGIS Enterprise Apache Airflow Provider",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Carlos Eduardo Mota",
    author_email="carlos.mota@sgb.gov.br",
    url="https://github.com/nds-cprm/airflow-arcgis-enterprise-provider",
    license="GPL",
    packages=[
        'airflow.providers.arcgis',
        'airflow.providers.arcgis.hooks'
    ],
    include_package_data=True,
    install_requires=[
        "apache-airflow>=2.4.0",
        "arcgis==2.0.*",
        "beautifulsoup4==4.*"
    ],
)