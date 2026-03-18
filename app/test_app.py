import asyncio
from declare import Root,TaskSet,component,effect,ref,scope,state
# Effect is set up and cleaned up.
def test_effectSetUpCleanUp():
  effectA=None
  def setEffectA(a):
    nonlocal effectA
    effectA=a
  @component
  def App():
    @effect
    def _():
      setEffectA(0)
      yield
      setEffectA(1)
  with Root(App())as root:
    assert effectA==0
  assert effectA==1
# Root is cleaned up when exception is raised.
def test_rootCleanUpOnRaise():
  effectA=None
  def setEffectA(a):
    nonlocal effectA
    effectA=a
  @component
  def App():
    @effect
    def _():
      setEffectA(0)
      yield
      setEffectA(1)
  try:
    with Root(App())as root:
      assert effectA==0
      raise Exception()
  except Exception:
    ...
  assert effectA==1
# Effect is reset when variable changes.
def test_effectResetOnVariableChange():
  effectA=None
  def setEffectA(a):
    nonlocal effectA
    effectA=a
  @component
  def App(a):
    @effect
    def _():
      setEffectA(a)
      yield
  with Root(App(a=0))as root:
    assert effectA==0
    root.render(App(a=1))
    assert effectA==1
# State sets.
def test_stateSet():
  effectA=None
  def setEffectA(a):
    nonlocal effectA
    effectA=a
  @component
  def App():
    a,setA=state(0)
    @effect
    def _():
      setEffectA((a,setA))
      yield
  with Root(App())as root:
    assert effectA[0]==0
    effectA[1](1)
    assert effectA[0]==1
# List concept.
def test_listConcept():
  effectA=[]
  @component
  def Com(a):
    @effect
    def _():
      effectA.append(a)
      yield
  with Root([
    Com(a=0),
    Com(a=1),
  ])as root:
    assert effectA==[0,1]
# Component's result.
def test_componentsResult():
  effectA=[]
  @component
  def Com(a):
    @effect
    def _():
      effectA.append(a)
      yield
  @component
  def App(a):
    return[
      Com(a=a)
      for a in a
    ]
  with Root(App([0,1]))as root:
    assert effectA==[0,1]
# List concept is aligned.
def test_listConceptAlign():
  effectA=[]
  @component
  def Com(a):
    @effect
    def _():
      effectA.append(a)
      yield
  @component
  def App(a):
    return[
      Com(a=a)
      for a in a
    ]
  with Root(App([0,1]))as root:
    assert effectA==[0,1]
    root.render(App([0,2]))
    assert effectA==[0,1,2]
# List concept of list concept.
def test_listConceptOfListConcept():
  effectA=[]
  @component
  def Com(a):
    @effect
    def _():
      effectA.append(a)
      yield
  with Root([
    Com(a=0),
    [Com(a=1),Com(a=2),],
  ])as root:
    assert effectA==[0,1,2]
# Keyed concept is reused.
def test_keyedConceptReused():
  effectA=[]
  @component
  def Com(a):
    @effect
    def _():
      effectA.append(a)
      yield
  with Root([
    Com(key=0,a=0),
    Com(key=1,a=1),
  ])as root:
    root.render([
      Com(key=1,a=1),
      Com(key=0,a=0),
    ])
    assert effectA==[0,1]
# Run setter in effect setup.
def test_runSetterInEffectSetup():
  effectA=[]
  @component
  def Com():
    b,setB=state(0)
    @effect
    def _():
      if b<1:
        setB(b+1)
      yield
    @effect
    def _():
      effectA.append(b)
      yield
  with Root(Com())as root:
    assert effectA==[0,1]
# Nested setter calls.
def test_nestedSetterCalls():
  effectA=lambda:0
  @component
  def Com():
    b,setB=state(0)
    @effect
    def _():
      effectA.setB=setB
      yield
    @effect
    def _():
      if b==1:
        setB(2)
      yield
  with Root(Com())as root:
    effectA.setB(1)
# ref returns the same ref.
def test_refReturnSame():
  effectA=[]
  @component
  def App():
    b=ref([])
    @effect
    def _():
      effectA.append(b)
      yield
  with Root(App())as root:
    root.render(App())
    assert len(effectA)==1
# TaskSet
def test_taskSet():
  async def _():
    effectA=[]
    @component
    def App(taskSet):
      @effect
      def _():
        async def _():
          print('a')
        t=taskSet.create_task(_())
        yield
        t.cancel()
    async with TaskSet()as taskSet:
      with Root(App(taskSet))as root:
        ...
  asyncio.run(_())
# scope
def test_scope():
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
  assert'(a(b0)(b1))'==''.join(effectA)
# Rendering str raises AssertionError.
def test_str():
  try:
    Root('.')
  except AssertionError:
    ...
