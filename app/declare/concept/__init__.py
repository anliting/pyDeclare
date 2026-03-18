from collections.abc import Iterable
from .. import config
class Concept:
  __slots__='key'
  def __init__(self,key=None):
    self.key=key
  def erase(self,proof):...
  def make(self,oldConcept,oldProof):
    oldConcept.erase(oldProof)
null=Concept()
def unique(a):
  s=set()
  for b in a:
    if b in s:
      return False
    s.add(b)
  return True
class ListConcept(Concept):
  __slots__='a'
  def __init__(self,a,key=None):
    super().__init__(key)
    assert config.iLoveBugs or unique(a.key for a in a if a.key!=None)
    self.a=a
  def erase(self,proof):
    for c,p in zip(self.a,proof):
      c.erase(p)
  def make(self,oldConcept,oldProof):
    #if not isinstance(oldConcept,__class__):
    if not type(oldConcept)==__class__:
      super().make(oldConcept,oldProof)
      return[
        c.make(null,None)
        for c in self.a
      ]
    oldKeyIdx={
      c.key:i
      for i,c in enumerate(oldConcept.a)
      if c.key!=None
    }
    oldUsed=len(oldConcept.a)*[False]
    newUse=len(self.a)*[(null,None)]
    for i,newCon in enumerate(self.a):
      j=(
        i if i<len(oldConcept.a)and oldConcept.a[i].key==None else None
      )if newCon.key==None else oldKeyIdx.get(newCon.key)
      if j!=None:
        oldUsed[j]=True
        newUse[i]=oldConcept.a[j],oldProof[j]
    for c,p,used in zip(oldConcept.a,oldProof,oldUsed):
      if not used:
        c.erase(p)
    return[
      c.make(*use)
      for c,use in zip(self.a,newUse)
    ]
def normalizeConcept(a):
  assert config.iLoveBugs or not isinstance(a,str)
  return(
    Concept()                                 if a==None else
    ListConcept([*map(normalizeConcept,a)])   if isinstance(a,Iterable)else
    a
  )
Fragment=lambda*a,key=None:ListConcept([normalizeConcept(a)for a in a],key)
