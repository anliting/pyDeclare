import itertools
from .. import config
from ..Effect import Effect
from ..Proof import Proof
from ..concept import Concept,normalizeConcept,null
from ..funcToClosureCellContent import funcToClosureCellContent
from ..hook import hook
from ..sameDep import sameDep
sameDepList=lambda a,b:len(a)==len(b)and all(sameDep(a,b)for a,b in zip(a,b))
class RenderConcept(Concept):
  __slots__=('a','ka')
  def __init__(self,*a,key=None,**ka):
    super().__init__(key)
    self.a=a
    self.ka=ka
  def erase(self,proof):
    proof.alive=False
    for e in proof.space:
      if isinstance(e.val,Effect):
        e.val.cleanup()
    proof.resultConcept,proof.resultProof=(
      null,proof.resultConcept.erase(proof.resultProof)
    )
  def make(self,oldConcept,oldProof):
    if not(
      isinstance(oldConcept,__class__)and
      oldConcept.render==self.render
    ):
      super().make(oldConcept,oldProof)
      newProof=Proof(self)
      with hook(newProof,None)as newSpace:
        newResultConcept=normalizeConcept(self.render(*self.a,**self.ka))
      newProof.resultConcept,newProof.resultProof=(
        newResultConcept,
        newResultConcept.make(null,None)
      )
      for e in newSpace:
        if isinstance(e.val,Effect):
         e.val.setup()
      newProof.space=newSpace
      return newProof
    oldProof.concept=self
    with hook(oldProof,oldProof.space)as newSpace:
      newResultConcept=normalizeConcept(self.render(*self.a,**self.ka))
    assert(
      config.iLoveBugs or
      all(
        a and b and type(a.val)==type(b.val)
        for a,b in itertools.zip_longest(oldProof.space,newSpace)
      )
    )
    oldProof.resultConcept,oldProof.resultProof=(
      newResultConcept,
      newResultConcept.make(oldProof.resultConcept,oldProof.resultProof)
    )
    for e,f in zip(oldProof.space,newSpace):
      if isinstance(e.val,Effect):
        if not sameDepList(
          e.val.closureCellContents,funcToClosureCellContent(f.val.cb)
        ):
          e.val.cleanup()
          f.val.setup()
        else:
          f.val=e.val
    oldProof.space=newSpace
    return oldProof
def component(f):
  class _(RenderConcept):
    render=staticmethod(f)
  return _
