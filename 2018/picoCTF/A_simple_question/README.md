# A simple question - Web

In this challenge, we are presented with a page that asks us to answer a question. The first thing we do is check the source code and we find
```<!-- source code is in answer2.phps -->```


If we go to that file, it contains this code:
```php
<?php
  include "config.php";
  ini_set('error_reporting', E_ALL);
  ini_set('display_errors', 'On');

  $answer = $_POST["answer"];
  $debug = $_POST["debug"];
  $query = "SELECT * FROM answers WHERE answer='$answer'";
  echo "<pre>";
  echo "SQL query: ", htmlspecialchars($query), "\n";
  echo "</pre>";
?>
<?php
  $con = new SQLite3($database_file);
  $result = $con->query($query);

  $row = $result->fetchArray();
  if($answer == $CANARY)  {
    echo "<h1>Perfect!</h1>";
    echo "<p>Your flag is: $FLAG</p>";
  }
  elseif ($row) {
    echo "<h1>You are so close.</h1>";
  } else {
    echo "<h1>Wrong.</h1>";
  }
?>
```

First thing that came to mind is type juggling because of two equal signs instead of three but that doesn't work because we don't know the contents of $CANARY variable. Then we see that this is Blind SQL injection because it only echoes output to the user. Therfore I fire up sqlmap and run:

> sqlmap -r sql.req --threads=10 --level 5 --risk 3 --dbms=SQLite --dump

We know it's SQLite as backend because of this line in the code
> $con = new SQLite3($database_file);

From sqlmap, I get back that there is an answer "41AndSixSixths" in the database SQLite_masterdb. 

Entering the answer on the page gives us the flag: picoCTF{qu3stions_ar3_h4rd_73139cd9} 

You could also have created a Python script to bruteforce all characters and digits, and based on the response "You are so close", you could determine if that character or digit was a correct one.