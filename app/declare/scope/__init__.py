from ..concept import Concept,Fragment,null
from ..sameDep import sameDep
sameKa=lambda a,b:a.keys()==b.keys()and all(sameDep(a[k],b[k])for k in a)
def scope(f):
  class A(Concept):
    def __init__(self,*a,key=None,**ka):
      super().__init__(key)
      self.fragment=Fragment(*a)
      self.ka=ka
    def erase(self,proof):
      self.fragment.erase(proof['fragment'])
      try:
        next(proof['iterator'])
      except StopIteration:
        ...
      super().erase(proof)
    def make(self,oldConcept,oldProof):
      if not(isinstance(oldConcept,__class__)and sameKa(oldConcept.ka,self.ka)):
        oldConcept.erase(oldProof)
        super().make(null,None)
        proof={'iterator':f(**self.ka)}
        next(proof['iterator'])
        proof['fragment']=self.fragment.make(null,None)
        return proof
      oldProof['fragment']=self.fragment.make(
        oldConcept.fragment,
        oldProof['fragment']
      )
      return oldProof
  return A
