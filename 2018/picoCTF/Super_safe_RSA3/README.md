# Super Safe RSA 3 - Crypto

On this RSA challenge, we get the following:
```
c: 2214959746368961374343866619773680463913808855252144119575578619282028038148568609891198127966225495311682540323131579203618894145626046974546075970616339033486317429461235324910794466410074881752239541146624247745072518241741204968025293372054661473208051944193745386532992238774551013797836031291096741
n: 5564465787507426784189854287795264081761345977763964262369153883931335062166838686916377911069328789715623668583315372050520387414170383621534793892389463905512682152442890656361180400315699526374103389751180954335677791471685242043876553878553597343813515063304714971565013966010693181624796612216036537
e: 65537
```

Here we have a larger n so multiple primes RSA is the way here. We can get all factors on [Alpertron](https://www.alpertron.com.ar/ECM.HTM) 

Then we google multiple primes RSA and create this script
```python
c = 2214959746368961374343866619773680463913808855252144119575578619282028038148568609891198127966225495311682540323131579203618894145626046974546075970616339033486317429461235324910794466410074881752239541146624247745072518241741204968025293372054661473208051944193745386532992238774551013797836031291096741

n = 5564465787507426784189854287795264081761345977763964262369153883931335062166838686916377911069328789715623668583315372050520387414170383621534793892389463905512682152442890656361180400315699526374103389751180954335677791471685242043876553878553597343813515063304714971565013966010693181624796612216036537

e = 65537

p1 = 2175350609
p2 = 2182560491
p3 = 2196605027
p4 = 2209029391
p5 = 2466547367
p6 = 2510616961
p7 = 2588079563
p8 = 2704140821
p9 = 2736762829
p10 = 2796597043
p11 = 2809479437
p12 = 2829659713
p13 = 2837556643
p14 = 2858051057
p15 = 3032087491
p16 = 3042267581
p17 = 3063304267
p18 = 3102491383
p19 = 3219243151
p20 = 3284737447
p21 = 3392021827
p22 = 3789952469
p23 = 3812358577
p24 = 3858988619
p25 = 3864352469
p26 = 3877179469
p27 = 3910354507
p28 = 3985847791
p29 = 3990903569
p30 = 4041031661
p31 = 4069378073
p32 = 4203209281

primes = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, \
          p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, \
          p26, p27, p28, p29, p30, p31, p32]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# From https://crypto.stackexchange.com/questions/31109/rsa-enc-decryption-with-multiple-prime-modulus-using-crt
ts = []
xs = []
ds = []

for i in range(len(primes)):
	ds.append(modinv(e, primes[i]-1))

m = primes[0]

for i in range(1, len(primes)):
	ts.append(modinv(m, primes[i]))
	m = m * primes[i]

for i in range(len(primes)):
	xs.append(pow((c%primes[i]), ds[i], primes[i]))

x = xs[0]
m = primes[0]

for i in range(1, len(primes)):
	x = x + m * ((xs[i] - x % primes[i]) * (ts[i-1] % primes[i]))
	m = m * primes[i]


print hex(x%n)[2:-1].decode("hex")
```

This script prints the flag: picoCTF{p_&_q_n0_r_$_t!!_6725536}