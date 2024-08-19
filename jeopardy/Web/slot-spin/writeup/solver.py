import requests

HOST = "http://localhost:9012"

s = requests.Session()
for i in range(10):
    resp = s.post(f"{HOST}/slot.php", json={"reels": [100, 100, 100]})
    print(resp.content)