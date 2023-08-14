


class Node:
  def __init__(self, value, renderValue, upperParent, needy = False):
    self.upperParent = upperParent
    self.children = []
    self.realValue = value
    self.renderValue = renderValue
    self.needy = needy


  # recursively splits node
  def split(self, maxSplit = 2):
    if self.realValue == 1:
      return
    if maxSplit <= 1:
      return 
    for i in reversed(range(maxSplit - 1)):
      if self.realValue % (i + 2) == 0:
        childValue = self.realValue // (i+1)
        for i in range(i + 2):
          
          self.children.append(Node(childValue, childValue, self))
        for child in self.children:
          child.split()
    

    # value must be odd; so make it even and split with largest again. send one branch back
    # create a new parent that is needy
    self.renderValue = self.realValue + 1
    
    newParent = Node(self.value, )