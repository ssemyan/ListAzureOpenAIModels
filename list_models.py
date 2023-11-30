import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import re
import argparse
import concurrent.futures


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

def process_region(region, deployments, filter_string, client):
    models_response = client.models.list(location=region)
    model_list = [model for model in models_response if model.kind == "OpenAI"]
    
    results = []
    
    if not model_list:
        return results

    quota_response = client.usages.list(location=region)
    quota_lookup = {quota.name.value.replace("OpenAI.Standard.", "").lower(): quota.limit 
                    for quota in quota_response 
                    if quota.name.value.startswith("OpenAI.Standard.")}
    
    results.append(f"Models in {region}: {len(model_list)}")
    
    quota_exists = False
    for model in model_list:
        m = model.model
        if filter_string and filter_string not in m.name:
            continue
        quota = quota_lookup.get(m.name, 0)
        if quota == 0:
            continue
        quota_exists = True
        
        deployment_string = ""
        quota_used = 0
        for deployment in deployments:
            if deployment.model == f"{m.name}-{m.version}" and deployment.region == region:
                quota_used += deployment.capacity
                deployment_string += f"\n      Deployment: {deployment.name} Quota: {deployment.capacity} Resource Group: {deployment.resource_group} Resource: {deployment.resource}"

        quota_left = quota - quota_used
        results.append(f"   {m.name}-{m.version} Quota: {quota_left:.0f}/{quota:.0f}{deployment_string}")

    if not quota_exists:
        results.append("   No quota available for any models")
    
    return results

def main(filter_string=None):
    sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not sub_id:
        raise Exception("AZURE_SUBSCRIPTION_ID is not set")

    client = CognitiveServicesManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )
    deployments = []
    pattern = r'resourceGroups\/(.*?)\/providers'
    accounts_response = client.accounts.list()

    for account in accounts_response:
        match = re.search(pattern, account.id)
        resource_group_name = match.group(1)
        deployments_response = client.deployments.list(resource_group_name=resource_group_name, account_name=account.name)
        for deployment in deployments_response:
            deployments.append(Deployment(deployment.name, f"{deployment.properties.model.name}-{deployment.properties.model.version}", deployment.sku.capacity, account.location, resource_group_name, account.name))
    
    # Create ThreadPoolExecutor for parallel execution
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_region = {executor.submit(process_region, region, deployments, filter_string, client): region for region in regions}
        for future in concurrent.futures.as_completed(future_to_region):
            region = future_to_region[future]
            try:
                # Get result from future and print it
                region_results = future.result()
                for result in region_results:
                    print(result)
            except Exception as exc:
                print(f'{region} generated an exception: {exc}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process the filter parameter.')
    parser.add_argument('--filter', type=str, help='Filter string to search in model names')
    args = parser.parse_args()

    # Call main()
    main(filter_string=args.filter)