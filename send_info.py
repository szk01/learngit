import requests

url = "https://zhidi.sfyf.cn:1888/xml"

payload = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\r\n" \
          "<Control attribute=\"Query\">"\
          "<DeviceInfo/>"\
          "</Control>"

headers = {
    'content-type': "text/xml",
    'cache-control': "no-cache",
    'postman-token': "92214f1d-c5b8-edc4-23b3-14fc316105cc"
    }

#构造一个查询请求
response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)