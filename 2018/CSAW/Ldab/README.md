#Ldab - Web

On this website, we can search for users and groups and because of the hint in challenge title, we first try LDAP Injection. After checking OWASP page, we first try this injection

> http://web.chal.csaw.io:8080/index.php?search=*)(uid=*))(|(uid=*

This one worked and gave us the flag: flag{ld4p_inj3ction_i5_a_th1ng}