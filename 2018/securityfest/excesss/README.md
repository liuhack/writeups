# Excesss - Web
> This is some kind of reverse captcha to tell if the visitor is indeed a robot. Can you complete it?

We are presented with this view in the challenge:
![excess](https://i.imgur.com/rXmLy7o.png)

If we go to the ```?xss=hello``` link, we can see this in the source code:
```<script>var x ='hello'; var y = `hello`; var z = "hello";</script>```

To escapse our own code into that, we can try:
```'; alert(1); var a='``` 

But we get a text prompt back after trying that because there is a js file in the source code that contains this:
```window.alert = (x=>prompt("He confirm. He alert. But most of all he prompt."));```

This this means that it turns the alert box into a prompt. In order to retrieve the original alert function, we can use an iframe to restore an overridden function. We run this payload:
```';q=document.createElement("iframe");q.setAttribute("src","http://xss1.alieni.se:2999");document.body.appendChild(q).contentWindow.alert(1)//;```
which gives us the flag.