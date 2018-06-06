# Mr.reagan - Misc
> Agent Smith got this from Mr. Reagan, a EMP was activated nearby, or?

Firstly, the file we got looked like this:
```
mrreagan: DOS/MBR boot sector, code offset 0x52+2, OEM-ID "NTFS    ", sectors/cluster 8, Media descriptor 0xf8, sectors/track 63, heads 255, hidden sectors 128, dos < 4.0 BootSector (0x80), FAT (1Y bit by descriptor); NTFS, sectors/track 63, sectors 96255, $MFT start cluster 4010, $MFTMirror start cluster 2, bytes/RecordSegment 2^(-1*246), clusters/index block 1, serial number 0a2061d9b061d7211
```
Here we see that we got a NTFS filesystem, and we can try to recover deleted files and see if something is there. This can be done with the tool ntfsundelete:
```ntfundelete -u -m "*" mrreagan```
Then we get the following back after running that command:
```
38       FN..   100%  2018-05-30 07:55      4096  fil867B.tmp

Undeleted 'fil867B.tmp' successfully.

39       FR..   100%  2018-05-30 07:55         0  2.E
Undeleted '2.E' successfully.

40       FR..   100%  2018-05-30 07:55         0  1.E
Undeleted '1.E' successfully.

41       FR..   100%  2018-05-30 07:55         0  3.E
Undeleted '3.E' successfully.

42       FR..   100%  2018-05-30 07:51        13  $Info
Undeleted '$Info' successfully.

43       FR..   100%  2018-05-30 07:51        13  $Secure
Undeleted '$Secure' successfully.

44       FR..   100%  2018-05-30 07:51        13  $Boot
Undeleted '$Boot' successfully.

45       FR..   100%  2018-05-30 07:51        13  $Extend
Undeleted '$Extend' successfully.

46       FR..   100%  2018-05-30 07:51        13  $LogFile
Undeleted '$LogFile' successfully.

47       FR..   100%  2018-05-30 07:51        43  Morpheus.txt
Undeleted 'Morpheus.txt' successfully.

48       FR..   100%  2018-05-30 07:51        11  Tank.txt
Undeleted 'Tank.txt' successfully.

49       FR..   100%  2018-05-30 07:51        11  Dozer.txt
Undeleted 'Dozer.txt' successfully.

50       FR..   100%  2018-05-30 07:51        69  Trinity.txt
Undeleted 'Trinity.txt' successfully.

51       FR..   100%  2018-05-30 07:52        22  Neo.txt
Undeleted 'Neo.txt' successfully.


Files with potentially recoverable content: 14
```

The deleted files above contain the following information:
```
Neo.txt - What is the Matrix.
Trinity.txt - I was looking for an answer. It's the question that drives us mad.
Dozer.txt - 73656366
Tank.txt -  73656366
Morpheus.txt - This line is tapped, so I must be brief.
$Logfile - X2Y0azN9Cg
$Extend - VsNTNfdzRz
$Boot - bjN0MWNfcH
$Secure - NjdHIwbTRn
$Info - c2N0ZnszbD
```

Then we try to decode the content there which looks like base64 and we get the flag with:
```
echo "c2N0ZnszbDNjdHIwbTRnbjN0MWNfcHVsNTNfdzRzX2Y0azN9Cg" | base64 -d
```