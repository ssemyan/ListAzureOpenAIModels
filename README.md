# List Azure OpenAI Models
Python script to list the available OpenAI quota in a subscription by region. It returns the name and quota used and total in thousand TPM for each region. 

## Sample Output
```
Region               Model                          Quota Used (K)  Total Quota (K)
australiaeast        Dalle                          0               2              
australiaeast        gpt-35-turbo                   0               300            
australiaeast        gpt-4                          0               40             
australiaeast        gpt-4-turbo                    0               80             
australiaeast        gpt-4-32k                      0               80             
australiaeast        gptv                           0               30             
australiaeast        text-embedding-ada-002         0               350            
brazilsouth          text-embedding-ada-002         0               350            
canadaeast           gpt-35-turbo                   5               300            
canadaeast           gpt-4                          3               40   
```

In the example above, in canadaeast region of th 40K TPM quota for GPT-4, 3K are currently being used by deployed models.

The columns are fixed lengh so they can be easily imported into Excel or other tools.

## Prerequisites
`pip install -r requirements.txt`

This sample makes use of a service principal (AKA App Registration) to access Azure. Before runing the sample, create (or reuse)
a service principal and ensure the principal has the *Cognitive Services OpenAI User* role set at the subscription level.
Then set the values of the client ID, tenant ID, client secret, and subscription ID in the environment variables: **AZURE_CLIENT_ID**, 
**AZURE_TENANT_ID**, **AZURE_CLIENT_SECRET**, and **AZURE_SUBSCRIPTION_ID**. These can be set in *setenv.sh* file and then run the command:
`source ./setenv.sh` to set the environment variables in Linux. 

For more info about how to use service principals, please see:
https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
