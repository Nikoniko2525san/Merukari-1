import os
import requests

url = os.environ["DISCORD_WEBHOOK_URL"]

response = requests.post(
    url,
    json={"content": "Python requests test"},
    timeout=10,
)

print("ステータス:", response.status_code)
print("内容:", response.text)
