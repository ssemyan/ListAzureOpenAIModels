# List Azure OpenAI Models
Python script to list all the available OpenAI models and associated quota in a subscription by region. It returns the name and version of each model along with the quota available.

## Sample Output
    Models in northcentralus: 8
        ada 1 Quota: 0
        babbage 1 Quota: 0
        curie 1 Quota: 0
        davinci 1 Quota: 0
        gpt-35-turbo 0613 Quota: 300
        gpt-35-turbo-16k 0613 Quota: 300
        text-embedding-ada-002 2 Quota: 350
        whisper 001 Quota: 1

## Prerequisites
`pip install -r requirements.txt`

This sample makes use of a service principal (AKA App Registration) to access Azure. Before runing the sample, create (or reuse)
a service principal and ensure the principal has the *Cognitive Services OpenAI User* role set at the subscription level.
Then set the values of the client ID, tenant ID, client secret, and subscription ID in the environment variables: **AZURE_CLIENT_ID**, 
**AZURE_TENANT_ID**, **AZURE_CLIENT_SECRET**, and **AZURE_SUBSCRIPTION_ID**. These can be set in *setenv.sh* file and then run the command:
`source ./setenv.sh` to set the environment variables in Linux. 

For more info about how to use service principals, please see:
https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
