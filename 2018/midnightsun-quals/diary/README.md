# Diary - Misc
> We found a torn diary on the ground. It seems to belong to a local boy.

In this challenge, we got a git repository. The first thing we can do is trying ```git log``` and we got the following
```
commit 2fec4e955704bd60292a9f9169f05c3334e555f4 (HEAD -> master)
Author: Calle Svensson <calle.svensson@zeta-two.com>
Date:   Sat Apr 14 02:22:52 2018 +0200

    Added pencil to wishlist

commit b182065ebc321a5432ab89be1ef2240077b3fbec
Author: Calle Svensson <calle.svensson@zeta-two.com>
Date:   Sat Apr 14 02:20:25 2018 +0200

    April 14th
error: Could not read afe5a9b6a373add54d07d874fb08edeec4a740da
fatal: Failed to traverse parents of commit e7354a8187cd28c075e602f40380968d2865dcac
```
This reveals that the git repository is corrupted. We can try to use the Extractor tool from the following great repository: https://github.com/internetwache/GitTools

After running the extractor bash script on the git repository, we look around in the files we got and the file ```1-4e9a1fe2aeb76cd0ab2c3d232691b714146b0475``` contains this content which reveals the flag:
```
Hello!

This is my diary. There are many like it but this one is mine.

April 9th
Today was a good day. I ate some pie.

April 10th
I was a little bit sad today.

April 11th
Today I found a flag, it said: midnight{if_an_object_ref_falls_and_no_one_hears} that sounds very interesting.
```
