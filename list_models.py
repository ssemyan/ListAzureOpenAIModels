import os
import requests
import json
from azure.identity import DefaultAzureCredential

# create array of azure regions
regions = [
    "australiaeast",
    "brazilsouth",
    "canadacentral",
    "canadaeast",
    "eastus",
    "eastus2",
    "francecentral",
    "germanywestcentral",
    "italynorth",
    "japaneast",
    "koreacentral",
    "northcentralus",
    "norwayeast",
    "polandcentral",
    "southafricanorth",
    "southcentralus",
    "southindia",
    "swedencentral",
    "switzerlandnorth",
    "switzerlandwest",
    "uksouth",
    "westeurope",
    "westus",
    "westus3" ]

 # get the subscription ID from the environment
sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
if not sub_id:
    raise Exception("AZURE_SUBSCRIPTION_ID is not set")

# get the default credential based on the environment variables
credential = DefaultAzureCredential()

for region in regions:
    # api URL is based on the subscription ID and region
    url = f"https://management.azure.com/subscriptions/{sub_id}/providers/Microsoft.CognitiveServices/locations/{region}/usages?api-version=2023-05-01"

    api_call_headers = {'Authorization': 'Bearer ' + credential.get_token('https://management.azure.com/.default').token}
    api_call_response = requests.get(url, headers=api_call_headers)

    if api_call_response.status_code != 200:
        print(f"Error: {api_call_response.text}")
        exit()

    model_list = json.loads(api_call_response.text)['value']
    #print(json.dumps(response_obj, indent=4))
    
    print(f"Quota usage in {region.upper()}:")
    for sku in model_list:
        model_name = sku['name']['value']
        
        # ignore the AccountCount, FineTuned, and ProvisionedManaged quota
        if "AccountCount" not in model_name and "ProvisionedManaged" not in model_name and "FineTuned" not in model_name and "finetune" not in model_name and "fine-tune" not in model_name:
            print(f"   {model_name.replace('OpenAI.Standard.', ''):<30} {sku['currentValue']}/{sku['limit']}")
    