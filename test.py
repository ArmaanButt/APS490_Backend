import http.client

conn = http.client.HTTPConnection("localhost:5000")

payload = "{\n\t\"is_working\": true,\n\t\"size\": 100.23,\n\t\"is_enabled\": false\n}"

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "e68a9307-c5f1-2034-cf42-2fdcb8b2f466"
    }

conn.request("POST", "/targets", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
