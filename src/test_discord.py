import json
import os
import urllib.request

url = os.environ["DISCORD_WEBHOOK_URL"]

data = json.dumps({
    "content": "Python webhook test"
}).encode("utf-8")

request = urllib.request.Request(
    url,
    data=data,
    headers={
        "Content-Type": "application/json",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=10) as response:
        print("成功:", response.status)
except Exception as error:
    print("失敗:", error)
