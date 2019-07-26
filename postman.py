import requests

url = "180.175.33.122:8787"

payload = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n  <Control attribute=\"Query\">\n    <Deviceinfo/>\n  </Control>"
headers = {
    'content-type': "text/html",
    'cache-control': "no-cache",
    'postman-token': "63819baf-7cd0-48d7-ff43-f093805ccaf1"
    }

response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)