file_name = "File Contoh.txt.enc"

# Memecah nama file berdasarkan titik pertama
split_name = file_name.split(".", 1)
num_characters = len(split_name[1])

if num_characters == 10:
    file_name = file_name[:-7]
    # print(file_name)

if num_characters == 7:
    file_name = file_name[:-4]

split_name = file_name.split(".", 1)
print(split_name)
ext = split_name[1]
print(ext)
print(f"{num_characters}")
a = 8
b = 2
while b != 0:
    a, b = b, a % b

print(f"Nilai a: {a}")


def extended_gcd(e, m):
    if e == 0:
        return m, 0, 1
    else:
        gcd, x, y = extended_gcd(m % e, e)
        return gcd, y - (m // e) * x, x
        # return  gcd, x, y
e = 7
m = 20
contoh1 = (m // e)
contoh2 = (m % e)
hasil = extended_gcd(e, m)
print(hasil)
print(contoh1)
print(contoh2)
