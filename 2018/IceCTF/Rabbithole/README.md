#Rabbit hole - Stego

We get an image with an onion on it and first thing we try to do is running steghide command:
> steghide extract -sf rabbithole.jpg

This requires a password and the first thing I tried was onion which worked. The reason I tried this password was because there was an onion on the picture. Then I get a file called address.txt which contains:
> wsqxiyhn23zdi6ia

After trying a lot of tools and comparing picture with original picture without finding anything, I try to google "onion address" and then I find that this could be an onion address in Tor-browser. After downloading Tor, we go to
> http://wsqxiyhn23zdi6ia.onion

which gives us a page that in looks like this at top:

![encoded](https://puu.sh/Bwy2l/ecd7133746.png)

Next step took some time as well and after trying many encodings, base65536 worked. This gave us a zip file that contained an epub file. If we opened this epub file and looked through the pages, the flag was there in cleartext.

IceCTF{if_you_see_this_youve_breached_my_privacy}
