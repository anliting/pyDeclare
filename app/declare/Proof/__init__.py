class Proof:
  __slots__=(
    'alive',
    'concept',
    'resultConcept',
    'resultProof',
    'space',
  )
  def __init__(self,concept):
    self.alive=True
    self.concept=concept
