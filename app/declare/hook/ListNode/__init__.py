class ListNode:
  __slots__=('next','val')
  def __init__(self):
    self.next=self.val=None
  def __iter__(self):
    self=self.next
    while self:
      yield self
      self=self.next
