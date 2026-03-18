import contextlib
from .ListNode import ListNode
root=hookCtx=None
class HookCtx:
  __slots__=('proof','oldSpace','newSpace')
  def __init__(self,proof,oldSpace):
    self.proof=proof
    self.oldSpace=oldSpace
    self.newSpace=ListNode()
def use():
  if hookCtx.oldSpace:
    hookCtx.oldSpace=hookCtx.oldSpace.next
  hookCtx.newSpace.next=hookCtx.newSpace=ListNode()
  return root,hookCtx.proof,hookCtx.oldSpace,hookCtx.newSpace
@contextlib.contextmanager
def hook(proof,oldSpace):
  global hookCtx
  oldCtx=hookCtx
  hookCtx=HookCtx(proof,oldSpace)
  try:
    yield hookCtx.newSpace
  finally:
    hookCtx=oldCtx
@contextlib.contextmanager
def hookRoot(r):
  global root
  oldRoot=root
  root=r
  try:
    yield
  finally:
    root=oldRoot
