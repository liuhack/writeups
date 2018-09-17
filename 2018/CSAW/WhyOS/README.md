# WhyOS

In this challenge you were given an Apple program and a system log, with the implication that the flag is somewhere in the log. Since the system log was 23 MB large, it was not feasible to read everything manually. Quick searches for strings like "flag" revealed nothing. After reversing the program slightly, we found the following interesting bit:

```
/* @class CSAWRootListController */
-(void)setflag {
    stack[-4] = r7;
    stack[-8] = lr;
    r7 = sp - 0x8;
    sp = sp - 0x38;
    var_4 = self;
    var_8 = _cmd;
    var_10 = [[NSMutableDictionary alloc] initWithContentsOfFile:@"/var/mobile/Library/Preferences/com.yourcompany.whyos.plist"];
    if ([var_10 objectForKey:@"flag", @"flag"] != 0x0) {
            var_2C = [var_10 objectForKey:@"flag", _objc_msgSend];
    }
    else {
            var_2C = @"";
    }
    r0 = NSLog(@"%@", var_2C);
    sp = sp + 0x30;
    return;
}
```

The main thing to note here is this:

```
r0 = NSLog(@"%@", var_2C);
```

Which implies that the flag is logged by itself on a line. There was a hint that the flag was in non-standard format and only contained hexadecimal symbols (0-9 and a-f). Since a typical log entry by NSLog looks like this:

```
default 18:59:15.532974 -0400   tccd    PID[36186] is checking access for target PID[34312]
```

We know that we're looking for something that is 5 "words" long ("default", time, -0400, name, log content), with the last word only containing hexadecimal symbols.

After making a quick script which searched for such lines, we found the following:

```
default 19:12:18.884704 -0400   Preferences ca3412b55940568c5b10a616fa7b855e
```

The last word was the flag.
