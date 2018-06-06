# Everywhere - Stego
> Too much information to decode.

We are provided with a JPEG image and the first thing we try is to run strings on it, binwalk to see if there is any hidden content in the file but nothing was there. The steghide tool did not find anything either. Then we can try to open the JPEG in GIMP and play around with contrast and brightness. When the contrast and brightness is at maximum, the flag can be found in a column.  If this would not have worked, the next step would be to google some reverse image search and see if there is any similar image and compare them.