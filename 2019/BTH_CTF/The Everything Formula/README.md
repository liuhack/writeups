## The Everything Formula (500 pts) (Programming)
```
 UPDATE: 
DEFHIJLMT = 2324636527250855711654045402739135123153104358174121382343919777360708492307257872714852254581755075320090464060404824792426714102141626925472266487940544704900324249304336903063658330652784343118959580086291102988272270794873124507606281724133124589226762621058470871505367231718672666167199815971568619837207902846673891568864400968901859854611828508744376967831401619266835347761717745757125514454073688988108829922501307509317743255947382978772992
________________________
Flag is BTH_CTF{<answer>}. Answer is given if you get 10 in a row! Use this to control your answers:
http://keelyhill.github.io/tuppers-formula/ 

$ nc challenge.ctf.bth.se 59209 
```
This is about the self-referential [Tupper's formula](https://en.wikipedia.org/wiki/Tupper%27s_self-referential_formula). Luckily there are [scripts out there](https://gist.github.com/mrexcessive/1c22b23f04f9a3217d44) that calculate the Tupper number based on a png file allowing us to botch something like this together:

```python
# Creates an image based on the requested text, calculates the tupper number based on that and uploads it.
import socket
import os
import time
from PIL import Image, ImageDraw, ImageFont

def netcat(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    while 1:
        data = str(s.recv(1024))
        if len(data)<10:
            pass
        else:
            print(data)
            try:
                text= data.split("tupper k corresponding to: ")[1].split("\\n")[0]
                print("Sending", text)

                img = Image.new('RGB', (106, 17), color = 'white')

                d = ImageDraw.Draw(img)
                # A bold monospace font thats as big as possible should be easy to read for the OCR that's presumably running on the other end
                fnt = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf', 18) 
                d.text((10,-3), text, font=fnt, fill=(0,0,0))

                img.save('tupper.png')
                os.system("sync")
                time.sleep(0.2)

                tupper = os.popen('python2 tupper.py read tupper.png').read() # Calls the script mentioned above
                s.send(str.encode(tupper))
            except:
                pass
            
    print ("Connection closed.")
    s.close()

netcat("challenge.ctf.bth.se", 59209)
```

After completing 10 challenges we get a tupper number back, which when visualised gives the flag.
