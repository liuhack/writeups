# in out error - General skills

> Can you utlize stdin, stdout, and stderr to get the flag from this program?

First thing I try is to run this:
> echo "Please may I have the flag?" | ./in-out-error 2>/dev/null

But this gives us the song lyrics as output, so the flag is not in stdout. Then I change so it does not print stdout by running:
> echo "Please may I have the flag?" | ./in-out-error 1>/dev/null

This prints out the flag to us: picoCTF{p1p1ng_1S_4_7h1ng_85f6fd2c}