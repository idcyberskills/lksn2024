# Writeup

Perhatikan bahwa saat memanggil fungsi aes_bcebccbcbecbeb(), posisi iv dan datanya tertukar, sehingga ini hanya menjadi stream cipher dengan key tiap block berikutnya merupakan block ciphertext sebelumnya. Terdapat sedikit hint apabila kita mencoba mengenkripsi ulang ciphertext flagnya, maka block pertama akan menjadi flag utuh.
