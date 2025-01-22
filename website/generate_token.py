import requests

url = "https://iam.cloud.ibm.com/identity/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": "mQcZ64keqdIMaqdcDfQYz2QJjzCz0Aa6L6KMk1AOYh08"
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Access Token:", access_token)
else:
    print("Error:", response.status_code, response.text)