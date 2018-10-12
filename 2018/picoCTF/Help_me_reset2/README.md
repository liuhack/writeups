# Help Me Reset 2 - Web

In this challenge, we need to reset a password for a user. By going to the reset link, we need a username. We first try admin and some other names but they don't exist. If we go back to the homepage of the challenge and look in the source code, we find this HTML comment:
```html
<!--Proudly maintained by dial-->
```

Now we have a username and if I enter it, I get the security question
> What is you favorite hero?

Then I intercept the request and see there is a flask session cookie
```
.eJw9jcEKgzAMhl9Fcu5B3FTwBXbaE2wiWZtpmTaSVjyI774Uxi5J_vDlywF2E6GQoAOLsuCHwMDKMfrXTNA94M3sdGV5ZtE-kXCOP7Y3IH6c0mB5y5LSwBZJBocJoTugSNnhPM56dGmuZdtUbV2BUVAoi3cOjqTYecGg8XbXEifxy6rDiGI9PgP0p5LCYfw_Or8kYjut.DpNb4g.8AVlDjrqQ9tR_6JGM2cdwlgsLmI
```

I decode the cookie with this [tool](https://github.com/noraj/flask-session-cookie-manager) so I run this command:
```
python session_cookie_manager.py decode -c ".eJw9jcEKgzAMhl9Fcu5B3FTwBXbaE2wiWZtpmTaSVjyI774Uxi5J_vDlywF2E6GQoAOLsuCHwMDKMfrXTNA94M3sdGV5ZtE-kXCOP7Y3IH6c0mB5y5LSwBZJBocJoTugSNnhPM56dGmuZdtUbV2BUVAoi3cOjqTYecGg8XbXEifxy6rDiGI9PgP0p5LCYfw_Or8kYjut.DpNb4g.8AVlDjrqQ9tR_6JGM2cdwlgsLmI"
```

The decoded cookie looks looks like this:
```
{"current":"carmake","possible":["food","color","hero","carmake"],"right_count":0,"user_data":{" t":["dial","3640762752",0,"red","wonder woman","GM","shrimp","garcia\n"]},"wrong_count":0}
```

Here we see that the answers to the security questions are stored. So then I needed two answer 3 security questions and after that, I could set a new password for the user dial and login with that. Then I have the flag: picoCTF{i_thought_i_could_remember_those_34745314}