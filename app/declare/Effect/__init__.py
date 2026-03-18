from ..funcToClosureCellContent import funcToClosureCellContent
class Effect:
  __slots__=('closureCellContents','generator','cb')
  def __init__(self,cb):
    self.cb=cb
  def cleanup(e):
    try:
      next(e.generator)
    except StopIteration:
      ...
    del e.closureCellContents
    del e.generator
  def setup(e):
    e.closureCellContents=funcToClosureCellContent(e.cb)
    e.generator=e.cb()
    next(e.generator)
    del e.cb
