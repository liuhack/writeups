# Jeil - Web
> You are awesome at breaking into stuff, how about breaking out?

In this challenge, we need to break out of a Javascript jail. This is the source code of it:

```Javascript
var readline = require('readline');
var rl = readline.createInterface(process.stdin, process.stdout);

var Jail = (function() {
    var rv = {};

    function secretFuncUnguessable{{ENV_SECRET_0}}(a,b,c){
        if(a === '{{ENV_SECRET_1}}' && b === '{{ENV_SECRET_2}}' && c === '{{ENV_SECRET_3}}'){
            return true;
        }
    }

    function call(code) {
        var line = "";

        if(new RegExp(/[\[\]\.\\\+\-\/;a-zA-Z{}`'"\s]/).test(code)){
            console.log("Unrecognized code.");
            throw 123;
            return;
        }

        if(!(code.length == 32)){
            console.log("Incorrect code length.");
            throw 123;
            return;
        }

        arguments = undefined;

        ret = null;
        ret = eval("this.secretFuncUnguessable"+code);

        if(typeof ret == "function"){
            if(ret.call(this,'{{ENV_SECRET_1}}', '{{ENV_SECRET_2}}', '{{ENV_SECRET_3}}') === true){
                console.log("{{ENV_SECRET_FLAG}}");
            }else{
                console.log("Incorrect code.");
            }
        }else{
            console.log("Incorrect code.");
        }
        throw 123;
    };
    rv.call = call;
    rv.toString = function(){return rv.call.toString()};

    return rv;
})();

template = `|￣￣￣￣￣￣￣￣|  
|    Internal    |
|＿＿＿＿＿＿＿＿|
       ||
(\\__/) || 
(•ㅅ•) || 
/ 　 づ  
Code: `;

function ask(){
    rl.question(template,function(answer){
        Jail.call(answer);
    });
}

ask();
```

From this code, we can see that we need to fulfil the following:
- input must be 32 bytes
- chars must not be any of [\[\]\.\\\+\-\/;a-zA-Z{}`'"\s]
- need ret to become a function which returns true

Therefore, we remove the prefix by issuing it a value with = operator and random garbage. Then we use the ? ternary operator to get code execution again. Since the = operator returns true, we can use the "true case" of the ? operator to get code execution to create a lambda function with "=>". The payload that we needed was:
```=1?_1=>1==1:11111111111111111111```
