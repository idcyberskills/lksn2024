# Writeup

Ada fungsi get_LKSN_flag pada index.js yang dimana menggunakan algoritma perhitungan RSA biasa, kita bisa cek p1 dan p2 merupakan bilangan prima biasa.
Untuk mendapatkan goals flagnya, variabel `hr` perlu dikalkulasi.

Setelah mendapatkan nilai `hr` dalam bentuk BigInt (menambahkan `n` pada akhir), maka kita ubah saja nilai `hr`nya di dalam si fungsi get_LKSN_flag dan jalankan kembali jsnya menggunakan Chrome Dev Tools:
`Runner.prototype.get_LKSN_flag()` maka akan muncul flagnya.

Referensi:

* https://gist.github.com/JARVIS-AI/cfb916c7dc3bea73abf0edac42749ea8