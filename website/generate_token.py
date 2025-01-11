import requests

url = "https://iam.cloud.ibm.com/identity/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": "YxictQ_ngjhf6I5mgnsG5F645nI_LCBw11l3kZduhfhM"
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Access Token:", access_token)
else:
    print("Error:", response.status_code, response.text)