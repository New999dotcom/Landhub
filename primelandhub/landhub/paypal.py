import requests
import base64

client_id = "AdwMJNlOrhnNK9extPrNhUQTJv5dtX7yC8RSVHr3c64C_bHF8-3m6I8GdN2o4jo0S2uRyP9_MjabzVQt"
client_secret = "EDw1Ge_ve7qyJXLJYv0C5yqXTl4nJWXU2g9Q7wSF-XAZXTG5QV2cB8TJdxV5us0oFfD9YhcC39mqj7p3"

# Encode credentials in Base64
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# Test Sandbox
url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {"grant_type": "client_credentials"}

response = requests.post(url, headers=headers, data=data)
print("Sandbox Test:")
print(response.text)

# Test Live
url = "https://api-m.paypal.com/v1/oauth2/token"
response = requests.post(url, headers=headers, data=data)
print("Live Test:")
print(response.text)