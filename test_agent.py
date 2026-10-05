from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

token = credential.get_token(
    "https://cognitiveservices.azure.com/.default"
)

print("SUCCESS")
print(token.token[:50])
