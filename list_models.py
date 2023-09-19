# based on https://learn.microsoft.com/en-us/rest/api/cognitiveservices/accountmanagement/models/list?tabs=Python
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

"""
# PURPOSE
    This sample demonstrates how to list all models available in a subscription by region. It returns the name and version of each model.
# EXAMPLE OUTPUT
    Models in northcentralus: 7
        ada 1
        babbage 1
        curie 1
        davinci 1
        gpt-35-turbo 0613
        gpt-35-turbo-16k 0613
        text-embedding-ada-002 2
# PREREQUISITES
    pip install -r requirements.txt
# USAGE
    python list_models.py

    This sample makes use of a service principal (AKA Application to access Azure. Before runing the sample, create (or reuse)
    a service principal and ensure the principal has the 'Cognitive Services OpenAI User' role set at the subscription level.
    Then set the values of the client ID, tenant ID, client secret, and subscription ID in the environment variables: AZURE_CLIENT_ID, 
    AZURE_TENANT_ID, AZURE_CLIENT_SECRET, and AZURE_SUBSCRIPTION_ID. These can be set in the setenv.sh file and then run the command:
    'source ./setenv.sh' to set the environment variables. 
    
    For more info about how to use service principals, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""

# create array of azure regions
regions = [
    "australiaeast",
    "brazilsouth",
    "westus",
    "westus2",
    "westeurope",
    "northeurope",
    "southeastasia",
    "eastasia",
    "westcentralus",
    "southcentralus",
    "eastus",
    "eastus2",
    "canadacentral",
    "japaneast",
    "centralindia",
    "uksouth",
    "japanwest",
    "koreacentral",
    "francecentral",
    "northcentralus",
    "centralus",
    "southafricanorth",
    "uaenorth",
    "swedencentral",
    "switzerlandnorth",
    "switzerlandwest",
    "germanywestcentral",
    "norwayeast",
    "westus3",
    "jioindiawest",
    "qatarcentral",
    "canadaeast" ]

def main():
    sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not sub_id:
        raise Exception("AZURE_SUBSCRIPTION_ID is not set")

    client = CognitiveServicesManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )

    for region in regions:
        
        # get the models
        models_response = client.models.list(
            location=region
        )
        model_list = list(models_response)
        
        if len(model_list) == 0:
            # if no models in the region, just continue
            # print(f"No models in {region}")
            continue

        # get the quota
        quota_response = client.usages.list(
            location=region
        )

        # build quota lookup
        quota_lookup = dict()
        for quota in quota_response:
            if quota.name.value.startswith("OpenAI.Standard."):
                quota_name = quota.name.value.replace("OpenAI.Standard.", "").lower()
                quota_lookup[quota_name] = quota.limit

        print(f"Models in {region}: {len(model_list)}")
        for model in model_list:
            m = model.model
            quota = 0
            if m.name in quota_lookup:
                quota = quota_lookup[m.name]
            print(f"   {m.name} {m.version} Quota: {quota:.0f}")

if __name__ == "__main__":
    main()