def sameDep(a,b):
  ta=type(a)
  return ta is type(b)and(
    a==b if ta in(bool,bytes,float,int,str,tuple)else a is b
  )
