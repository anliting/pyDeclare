import collections
from . import config
from .RenderConcept import RenderConcept,component
from .Effect import Effect
from .State import State
from .TaskSet import TaskSet
from .concept import Concept,Fragment,normalizeConcept,null
from .hook import use,hookRoot
from .scope import scope
def effect(cb):
  _,_,_,newSlot=use()
  newSlot.val=Effect(cb)
class Ref:
  __slots__='val'
  def __init__(self,val):
    self.val=val
def ref(a):
  _,_,oldSlot,newSlot=use()
  newSlot.val=oldSlot.val if oldSlot else Ref(a()if callable(a)else a)
  return newSlot.val
def state(a):
  root,proof,oldSlot,newSlot=use()
  if oldSlot:
    assert config.iLoveBugs or isinstance(oldSlot.val,State)
    newSlot.val=oldSlot.val
  else:
    def _(a):
      def _():
        if not proof.alive:
          return
        newSlot.val.val=a(newSlot.val.val)if callable(a)else a
        proof.concept.make(proof.concept,proof)
      root._enqueue(_)
    newSlot.val=State(a()if callable(a)else a,_)
  return newSlot.val.val,newSlot.val.setter
class SyncScheduler:
  __slots__=('_flushing','_root')
  def __init__(self,root):
    self._flushing=False
    self._root=root
  def flush(self):
    if self._flushing:
      return
    self._flushing=True
    try:
      self._root._flush()
    finally:
      self._flushing=False
  def onEnqueue(self):
    self.flush()
class Root:
  __slots__=('_concept','_proof','_queue','_scheduler')
  def __init__(self,concept=None,schedulerFactory=None):
    self._queue=collections.deque()
    self._concept,self._proof=null,None
    self._scheduler=(schedulerFactory or SyncScheduler)(self)
    self.render(concept)
  __enter__=lambda self:self
  def __exit__(self,exc_type,exc,tb):
    self.close()
  def _enqueue(self,f):
    self._queue.append(f)
    self._scheduler.onEnqueue()
  def _flush(self):
    with hookRoot(self):
      while self._queue:
        self._queue.popleft()()
  def close(self):
    self.render(None)
  def render(self,concept):
    concept=normalizeConcept(concept)
    def _():
      self._concept,self._proof=concept,concept.make(
        self._concept,self._proof
      )
    self._enqueue(_)
def iLoveBugs():
  config.iLoveBugs=True
