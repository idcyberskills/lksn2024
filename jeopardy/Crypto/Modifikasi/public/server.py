from hashlib import md5

print("Anda sedang menjual tiket konser taylor swift")
print("Terdapat 2 pembeli yang ingin membeli tiket, Alice dan Bob. Sayangnya tiket hanya tersisa 1")
print("Tiket tersebut diverifikasi menggunakan md5")
print("Dapatkah anda membuat tiket palsu untuk dijual ke Bob?")

alice = bytes.fromhex(input("Masukkan kode tiket untuk dijual ke Alice: "))
if not alice.startswith(b"TIKETTAYLORSWIFTASLI"):
    print("Kode tiket tidak valid")
    exit()

md5alice = md5(alice).digest()
print("md5 dari tiket Alice:", md5alice.hex())

bob = bytes.fromhex(input("Masukkan kode tiket buatan untuk dijual ke Bob: "))
md5bob = md5(bob).digest()
if alice == bob:
    print("Bob: Hey apa apaan ini, ini sama persis dengan tiket Alice!")
    exit()

print("md5 dari tiket Bob:", md5bob.hex())
if alice != bob and md5bob == md5alice:
    print("Bob: Terima kasih! Ini bayarannya")
    print(open("flag.txt").read())
else:
    print("Bob: Hey apa apaan ini, ini bukan tiket asli!")