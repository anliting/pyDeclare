import asyncio
import time
from ..declare import Concept,Fragment,TaskSet,Root,component,effect,normalizeConcept,null,ref,scope,state
effectA=[]
@component
def B(a):
  @effect
  def _():
    effectA.append(f'(b{a}')
    yield
    effectA.append(')')
@scope
def A():
  effectA.append('(a')
  yield
  effectA.append(')')
with Root(A(B(0)))as root:
  root.render(A(B(1)))
print('(a(b0)(b1))'==''.join(effectA))
