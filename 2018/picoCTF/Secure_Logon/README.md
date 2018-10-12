# Secure Logon - Web

We are presented with a webpage and source code to it. The source code we get is the following:
```python
from flask import Flask, render_template, request, url_for, redirect, make_response, flash
import json
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES

app = Flask(__name__)
app.secret_key = 'seed removed'
flag_value = 'flag removed'

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form['user'] == 'admin':
        message = "I'm sorry the admin password is super secure. You're not getting in that way."
        category = 'danger'
        flash(message, category)
        return render_template('index.html')
    resp = make_response(redirect("/flag"))

    cookie = {}
    cookie['password'] = request.form['password']
    cookie['username'] = request.form['user']
    cookie['admin'] = 0
    print(cookie)
    cookie_data = json.dumps(cookie, sort_keys=True)
    encrypted = AESCipher(app.secret_key).encrypt(cookie_data)
    print(encrypted)
    resp.set_cookie('cookie', encrypted)
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('cookie', '', expires=0)
    return resp

@app.route('/flag', methods=['GET'])
def flag():
  try:
      encrypted = request.cookies['cookie']
  except KeyError:
      flash("Error: Please log-in again.")
      return redirect(url_for('main'))
  data = AESCipher(app.secret_key).decrypt(encrypted)
  data = json.loads(data)

  try:
     check = data['admin']
  except KeyError:
     check = 0
  if check == 1:
      return render_template('flag.html', value=flag_value)
  flash("Success: You logged in! Not sure you'll be able to see the flag though.", "success")
  return render_template('not-flag.html', cookie=data)

class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')

if __name__ == "__main__":
    app.run()
```

If we login on the webpage with username: ' or 1=1# and password "test", we come to this page:
![loggedIn](https://puu.sh/BIfR9/7235b7b714.png)

This challenge is about AES with CBC mode. Decryption of AES-CBC ciphertext involves decrypting each block of ciphertext with AES, then performing an XOR operation between the AES-decrypted block and the previous block of ciphertext. For the first block, there is no previous ciphertext block and as such the Initialization Vector (IV), a random block-sized piece of data, is used. Wikipedia has a nice diagram of the process:
![cbc](https://puu.sh/BIfYY/14bcb546fc.png)


AES with CBC is vulnerable to bit flipping attack. By flipping a bit in a ciphertext block, we can flip the output plaintext bit of the next block. Why? Because XOR is an associative bit operation, and XOR-ing with ‘1’ changes a ‘0’ to ‘1’ and vice versa, by the definition of XOR.

With this information, we can create a script to flip the byte 0 to 1. But it needed a bit of trial and error because we needed to find the offset for the byte to be flipped, and after increasing it, offset 10 worked. The following script will give us our updated cookie:

```python
import base64

cookie = base64.b64decode("4Ol7IYySLlyrKHeIo7UFtoVhkpQ7gmkscYXp8ctZwmroUWhof9YrZYYURyM2TpLze6bO/Vpo40rJ4R1zQXg/yzZe0mUopeHZ+dztZGm51vI=")
flip = ord(cookie[10]) ^ ord("0") ^ ord("1")
newCookie = base64.b64encode(cookie[:10]+chr(flip)+cookie[11:])
print newCookie
```

Then we get our cookie
```4Ol7IYySLlyrKHaIo7UFtoVhkpQ7gmkscYXp8ctZwmroUWhof9YrZYYURyM2TpLze6bO/Vpo40rJ4R1zQXg/yzZe0mUopeHZ+dztZGm51vI=```

After updating it on the webpage, we get the flag: picoCTF{fl1p_4ll_th3_bit3_7d7c2296}
