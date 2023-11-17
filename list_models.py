import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import re

# create array of azure regions
regions = [
    "southindia",
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

class Deployment:
    def __init__(self, name, model, capacity, region, resource_group, resource):
        self.name = name
        self.model = model
        self.capacity = capacity
        self.region = region
        self.resource_group = resource_group
        self.resource = resource

def main():
    sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not sub_id:
        raise Exception("AZURE_SUBSCRIPTION_ID is not set")

    client = CognitiveServicesManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )

    # get all the deployments
    deployments = []
    # sample account ID '/subscriptions/abcd1234-1234-5678-9012-098330bfffff/resourceGroups/OpenAI/providers/Microsoft.CognitiveServices/accounts/myaccount'
    # Regex pattern to extract resource group name
    pattern = r'resourceGroups\/(.*?)\/providers'

    accounts_response = client.accounts.list()
    for account in accounts_response:
        #print(account.name)
        # get resource group from account
        match = re.search(pattern, account.id)
        resource_group_name = match.group(1)
        deployments_response = client.deployments.list(
            resource_group_name = resource_group_name,
            account_name = account.name
        )
        for deployment in deployments_response:
            deployments.append(Deployment(deployment.name, f"{deployment.properties.model.name}-{deployment.properties.model.version}", deployment.sku.capacity, account.location, resource_group_name, account.name))
            #print(f"{deployment.name} - Model: {deployment.properties.model.name} Quota: {deployment.sku.capacity}")

    for region in regions:
        
        # get the models
        models_response = client.models.list(
            location=region
        )
        model_list = list()
        for model in models_response:
            if model.kind == "OpenAI":
                model_list.append(model)
        
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

            # show any deployments
            deployment_string = ""
            quota_used = 0
            for deployment in deployments:
                if deployment.model == f"{m.name}-{m.version}" and deployment.region == region:
                    quota_used = quota_used + deployment.capacity
                    deployment_string = deployment_string + f"\n      Deployment: {deployment.name} Quota: {deployment.capacity} Resource Group: {deployment.resource_group} Resource: {deployment.resource}"

            quota_left = quota - quota_used
            print(f"   {m.name}-{m.version} Quota: {quota_left:.0f}/{quota:.0f}{deployment_string}")

if __name__ == "__main__":
    main()