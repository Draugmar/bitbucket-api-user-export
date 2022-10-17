import requests
from datetime import datetime
from csv import writer
from base64 import b64encode

url = "https://BitbucketServerUrl/rest/api/1.0/admin/users?limit=150"
out = writer(open("bitbucket_users.csv","w",newline=''), delimiter=",")

out.writerow(["name","email","displayName","active","lastAuthenticationTimestamp"])

userAndPass = b64encode(b"username:password").decode("ascii")

payload = {}
headers = {
  'Authorization': 'Basic %s' % userAndPass 
}

response = requests.get(url, headers=headers, data = payload)

data = response.json()

for row in data['values']:
    if "lastAuthenticationTimestamp" in row:
        dt_lastAuthentication = datetime.fromtimestamp(int(row['lastAuthenticationTimestamp'])/1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        dt_lastAuthentication = "unknown"

    out.writerow([row["name"],row["emailAddress"],row["displayName"],row["active"],dt_lastAuthentication])

