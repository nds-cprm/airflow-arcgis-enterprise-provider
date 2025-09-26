import io
from os.path import dirname, join
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf-8")
    ).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

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
        'airflow.providers.arcgis_enterprise',
        'airflow.providers.arcgis_enterprise.hooks'
    ],
    include_package_data=True,
    install_requires=required,
    entry_points={
        'apache_airflow_provider': [
            "provider_info=airflow.providers.arcgis_enterprise.__init__:get_provider_info"
        ],
    },
)