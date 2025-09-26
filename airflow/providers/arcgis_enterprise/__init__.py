from typing import Dict, Any

PROVIDER_PACKAGE_NAME = "apache-airflow-providers-arcgis"
PROVIDER_NAME = "ArcGIS Online/ArcGIS Enterprise sUNGA"
PROVIDER_DESCRIPTION = "ArcGIS Online/ArcGIS Enterprise blah <https://www.arcgis.com/>"

with open('requirements.txt') as f:
    required = f.read().splitlines()

def get_provider_info() -> Dict[str, Any]:
    return {
        # O ID do pacote é usado pelo Airflow
        "package-name": PROVIDER_PACKAGE_NAME,
        # O nome de exibição na UI
        "name": PROVIDER_NAME,
        "description": PROVIDER_DESCRIPTION,
        "versions": ["1.0.0"],
        "dependencies": required,
        # "integrations": [
        #     {
        #         "integration-name": "ArcGIS Online/ArcGIS Enterprise",
        #         "external-doc-url": "https://developers.arcgis.com/python/api-reference/",
        #         "logo": "/integration-logos/ftp/FTP.png",
        #         "tags": [
        #             "service"
        #         ]
        #     }
        # ],
        
        # A parte mais importante: define o novo tipo de conexão
        "connection-types": [
            {
                "connection-type": 'arcgis',
                "hook-class-name": "airflow.providers.arcgis_enterprise.hooks.arcgis.ArcGISHook"
            }
        ],

        "hooks": [
            {
                "integration-name": "ArcGIS Online/ArcGIS Enterprise",
                "python-modules": [
                    "airflow.providers.arcgis_enterprise.hooks.arcgis"
                ]
            }
        ]
        
        # # Você pode listar os Operators para documentação/referência
        # "operators": [
        #     {
        #         "class-name": "airflow.providers.arcgis_enterprise.operators.arcgis.ArcGISOperator"
        #     }
        # ],
    }