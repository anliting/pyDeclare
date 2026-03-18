class State:
  __slots__=('setter','val')
  def __init__(self,val,setter):
    self.setter=setter
    self.val=val
