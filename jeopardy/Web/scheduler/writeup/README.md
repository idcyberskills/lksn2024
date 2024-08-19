# Writeup

Fungsi `Extract` Django memanfaatkan fungsi bawaan DBMS. Apabila parameter `lookup_name` tidak dihandle, maka dapat terjadi SQL injection. Dikarenakan website menggunakan postgreSQL, maka fungsi payloadnya injection berdasarkan extract function di postgreSQL.

Solver `errbase` memanfaatkan error biginteger, sedangkan `timebase` memanfaatkan sleep function dan mengukur lama request di proses.