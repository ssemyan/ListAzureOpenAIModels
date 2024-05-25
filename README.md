# List Azure OpenAI Models
Python script to list the available OpenAI quota in a subscription by region. It returns the name and quota available each model. For example, 70/240 means that 70K TPM out of 250K TPM have been allocated to deployments.

## Sample Output
```
    Quota usage in francecentral:
        Model: gpt-35-turbo                        70/240
        Model: gpt-4                               10/20
        Model: gpt-4-turbo                         10/80
        Model: gpt-4-32k                           0/60
        Model: text-embedding-ada-002              0/240
        Model: text-embedding-3-large              0/350
```

## Prerequisites
`pip install -r requirements.txt`

This sample makes use of a service principal (AKA App Registration) to access Azure. Before runing the sample, create (or reuse)
a service principal and ensure the principal has the *Cognitive Services OpenAI User* role set at the subscription level.
Then set the values of the client ID, tenant ID, client secret, and subscription ID in the environment variables: **AZURE_CLIENT_ID**, 
**AZURE_TENANT_ID**, **AZURE_CLIENT_SECRET**, and **AZURE_SUBSCRIPTION_ID**. These can be set in *setenv.sh* file and then run the command:
`source ./setenv.sh` to set the environment variables in Linux. 

For more info about how to use service principals, please see:
https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
