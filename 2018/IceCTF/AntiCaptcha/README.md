#AntiCaptcha

For this challenge you were given a rather long form with questions to be filled in. Most of the questions were of of the following types:

>What is the greatest common divisor of 2052 and 5816?
>What is the 2nd word in the following line: for job bring next mention prove. maybe let thank show. live recent i seek. arrive stay draw save thought exist. manage number drug eye tough kind.
>Is 5174 a prime number?

With what appears to be randomized sequences of words and numbers.

There were also a few special questions which didn't fit into this format, such as:

>What is the capital of Hawaii?
>Who directed the movie Jaws?

Thinking you were supposed to fill in the form automatically, I created some javascript code which could simply be pasted into the console. It seemed to fill in the answer to every question just fine, but when I ran it I got "200 answers wrong". This was a bit strange. When I ran just pressed submit I got "6 answers wrong", so clearly something is going on here. I then realized that there was only 6 special questions. When I filled in the answer to just those, I got the flag.

IceCTF{ahh\_we\_have\_been\_captchured}
