## Cryptor (500 pts) (Reversing)
```
Found this string together with the attached dll file. Can you make sense of it?
snV4POQVgfNHXr/hIaS5vkD77Sz8RkrR3JHXUkG1IAk= 

given: a .dll-file named cryptor.dll
```

Running the cryptor.dll through the Jetbrains Decompiler gave us the following:

```
// Decompiled with JetBrains decompiler
// Type: cryptor.Cryptor
// Assembly: cryptor, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null
// MVID: 056E43BF-4823-4E48-AF0C-783AF8C59216

using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace cryptor
{
  public static class Cryptor
  {
    private const string initVector = "pemgail9uzpgzl88";
    private const int keysize = 256;

    public static string EncryptString(string plainText, string passPhrase)
    {
      byte[] bytes1 = Encoding.UTF8.GetBytes("pemgail9uzpgzl88");
      byte[] bytes2 = Encoding.UTF8.GetBytes(plainText);
      byte[] bytes3 = new PasswordDeriveBytes(passPhrase, (byte[]) null).GetBytes(32);
      RijndaelManaged rijndaelManaged = new RijndaelManaged();
      rijndaelManaged.Mode = CipherMode.CBC;
      ICryptoTransform encryptor = rijndaelManaged.CreateEncryptor(bytes3, bytes1);
      MemoryStream memoryStream = new MemoryStream();
      CryptoStream cryptoStream = new CryptoStream((Stream) memoryStream, encryptor, CryptoStreamMode.Write);
      cryptoStream.Write(bytes2, 0, bytes2.Length);
      cryptoStream.FlushFinalBlock();
      byte[] array = memoryStream.ToArray();
      memoryStream.Close();
      cryptoStream.Close();
      return Convert.ToBase64String(array);
    }
 
    public static string getKey()
    {
      return Cryptor.EncryptString("CDC security link", "32GGH&&T53¤.,l¤¤rfs#");
    }

    public static string DecryptString(string cipherText, string passPhrase)
    {
      byte[] bytes1 = Encoding.UTF8.GetBytes("pemgail9uzpgzl88");
      byte[] buffer = Convert.FromBase64String(cipherText);
      byte[] bytes2 = new PasswordDeriveBytes(passPhrase, (byte[]) null).GetBytes(32);
      RijndaelManaged rijndaelManaged = new RijndaelManaged();
      rijndaelManaged.Mode = CipherMode.CBC;
      ICryptoTransform decryptor = rijndaelManaged.CreateDecryptor(bytes2, bytes1);
      MemoryStream memoryStream = new MemoryStream(buffer);
      CryptoStream cryptoStream = new CryptoStream((Stream) memoryStream, decryptor, CryptoStreamMode.Read);
      byte[] numArray = new byte[buffer.Length];
      int count = cryptoStream.Read(numArray, 0, numArray.Length);
      memoryStream.Close();
      cryptoStream.Close();
      return Encoding.UTF8.GetString(numArray, 0, count);
    }
  }
}
```

The EncryptString method takes plaintext and a passphrase, and returns a base64-encoded ciphertext. The DecryptString methods takes a base64-encoded ciphertext and a passphrase, and returns the plaintext.

It is clear that we're supposed to decrypt the given base64-encoded string.

For a long time, we thought that the getKey-method was a clue to what the passphrase was, so we tried to call `DecryptString("snV4POQVgfNHXr/hIaS5vkD77Sz8RkrR3JHXUkG1IAk=", "32GGH&&T53¤.,l¤¤rfs#");`.
Unfortunately, this did not work because of padding errors. When we changed the decrypt method to use a different padding we only got garbage in return.

After a while we figured out that the getKey() method returned the passphrase to be used, and calling `DecryptString("snV4POQVgfNHXr/hIaS5vkD77Sz8RkrR3JHXUkG1IAk=", getKey());` gave us the flag.
