# Every node has a list of child nodes, and a main parent node.
# the first parent of the child gets added to the start of parents list.
# every node has a math value and a display value
# Can choose Trouhgput Limited or Throughput unlimited (TL / TU)
# a node will split until reaches a size of 1

class Node:
  count = 0
  def __init__(self, max_split, max_merge, mathValue, parent = None, needy = False):
    assert max_split >= 2
    assert max_merge >= 2
    assert mathValue >= 1

    Node.count += 1
    self.id = Node.count

    self.parents = [parent]
    self.max_merge = max_merge
    self.max_split = max_split
    self.mathValue = mathValue
    self.children = []
    self.needy = needy
    self.beenSplit = False

  def __str__(self):
    return str(self.id)

  def fillNeedy(self):
    current = self.parents[0]
    while current != None:
      if current.needy:
        self.children.append(current)
        current.parents.append(self)
        current.needy = False
        return True
      current = current.parents[0]
    return False
  
  def split(self):
    if self.mathValue == 1:
      return
    if self.beenSplit:
      return
    self.beenSplit = True
    for i in reversed(range(self.max_split - 1)):
      if self.mathValue % (i + 2) == 0:
        for j in range(i + 2):
          if self.mathValue // (i + 2) == 1:
            if not self.fillNeedy():
              self.children.append(Node(self.max_split, self.max_merge, self.mathValue // (i + 2), self))
          else:
            self.children.append(Node(self.max_split, self.max_merge, self.mathValue // (i + 2), self))
        for child in self.children:
          child.split()
        return
    
    # it is not splitable nicely so we add 1
    self.mathValue += 1
    
    # create new parent
    newParent = Node(self.max_split, self.max_merge, self.mathValue, self.parents[0], True)
    newParent.beenSplit = True
    
    # replace child from parent
    if self.parents[0]:
      for i, child in enumerate(self.parents[0].children):
        if child == self:
          self.parents[0].children[i] = newParent

    newParent.children.append(self)
    self.parents[0] = newParent
        


    for i in reversed(range(self.max_split - 1)):
      if self.mathValue % (i + 2) == 0:
        for j in range(i + 2):
          if self.mathValue // (i + 2) == 1:
            if not self.fillNeedy():
              self.children.append(Node(self.max_split, self.max_merge, self.mathValue // (i + 2), self))
          else:
            self.children.append(Node(self.max_split, self.max_merge, self.mathValue // (i + 2), self))
        for child in self.children:
          child.split()
        return

  def getDigraphLabel(self):
    if self.parents[0] == None:
      shape = 'house'
    
    elif len(self.parents) > 1:
      shape = 'square'
    elif self.mathValue == 1:
      shape = 'invhouse'
    else:
      shape = 'diamond'
      
    return str(self.id) + ' [label="' + str(self.mathValue) + '" shape="' + shape + '"];\n'
  
  def getDigraphConnections(self):
    connections = []
    for child in self.children:
      connections.append(str(self.id) + '->' + str(child.id) + '[label="' + str(self.mathValue // len(self.children)) + '"];\n')
    return connections
  

def createTree(n, maxSplit, maxMerge):
  Node.count = 0
  headNode = Node(maxSplit, maxMerge, n)
  headNode.children.append(Node(maxSplit, maxMerge, n, headNode))
  headNode.children[0].split()
  return headNode





def getAllLabelsAndConnects(node, explored, labels, connections):
  if node in explored:
    return
  explored.append(node)
  labels.append(node.getDigraphLabel())

  for e in node.getDigraphConnections():
    connections += e

  for child in node.children:
    getAllLabelsAndConnects(child, explored, labels, connections)
  
def drawTree(root):
  graphvizString = "digraph G {"
  labels = []
  connections = []
  explored = []

  getAllLabelsAndConnects(root, explored, labels, connections)
  for e in labels:

    graphvizString += e
  for e in connections:
    graphvizString += e
  
  graphvizString += "}"
  print(graphvizString)


  

tree = createTree(11, 3, 3)
drawTree(tree)