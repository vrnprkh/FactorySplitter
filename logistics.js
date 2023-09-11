class TreeNode {
  static count = 0;

  constructor(maxSplit, maxMerge, mathValue, parent = null, needy = false) {
    if (maxSplit < 2 || maxMerge < 2 || mathValue < 1) {
      throw new Error('Invalid input values');
    }

    TreeNode.count += 1;
    this.id = TreeNode.count;

    this.parents = [parent];
    this.maxMerge = maxMerge;
    this.maxSplit = maxSplit;
    this.mathValue = mathValue;
    this.children = [];
    this.needy = needy;
    this.beenSplit = false;
  }

  toString() {
    return String(this.id);
  }

  fillNeedy() {
    let current = this.parents[0];
    while (current !== null) {
      if (current.needy) {
        this.children.push(current);
        current.parents.push(this);
        current.needy = false;
        return true;
      }
      current = current.parents[0];
    }
    return false;
  }

  addChild(value) {
    this.children.push(new TreeNode(this.maxSplit, this.maxMerge, value, this));
  }

  trySplitting() {
    for (let i = this.maxSplit - 2; i >= 0; i--) {
      if (this.mathValue % (i + 2) === 0) {
        for (let j = 0; j < i + 2; j++) {
          if (this.mathValue / (i + 2) === 1) {
            if (!this.fillNeedy()) {
              this.addChild(this.mathValue / (i + 2));
            }
          } else {
            this.addChild(this.mathValue / (i + 2));
          }
        }
        for (const child of this.children) {
          child.split();
        }
        return true;
      }
    }
    return false;
  }

  split() {
    if (this.mathValue === 1) {
      return;
    }
    if (this.beenSplit) {
      return;
    }
    this.beenSplit = true;
    if (this.trySplitting()) {
      return;
    }
    // It is not splittable nicely, so we add 1
    this.mathValue += 1;
    // Create a new parent
    const newParent = new TreeNode(this.maxSplit, this.maxMerge, this.mathValue, this.parents[0], true);
    newParent.beenSplit = true;
    // Replace child from parent
    if (this.parents[0] !== null) {
      for (let i = 0; i < this.parents[0].children.length; i++) {
        if (this.parents[0].children[i] === this) {
          this.parents[0].children[i] = newParent;
        }
      }
    }
    newParent.children.push(this);
    this.parents[0] = newParent;
    if (!this.trySplitting()) {
      throw new Error('Splitting failed');
    }
  }

  getDigraphLabel() {
    let shape = 'house';
    if (this.parents[0] === null) {
      shape = 'house';
    } else if (this.parents.length > 1) {
      shape = 'square';
    } else if (this.mathValue === 1) {
      shape = 'invhouse';
    } else {
      shape = 'diamond';
    }
    return `${this.id} [label="${this.mathValue}" shape="${shape}"];\n`;
  }

  getDigraphConnections() {
    const connections = [];
    for (const child of this.children) {
      connections.push(`${this.id}->${child.id} [label="${this.mathValue / this.children.length}"];\n`);
    }
    return connections;
  }
}

function createTree(n, maxSplit, maxMerge) {
  TreeNode.count = 0;
  const headNode = new TreeNode(maxSplit, maxMerge, n);
  headNode.children.push(new TreeNode(maxSplit, maxMerge, n, headNode));
  headNode.children[0].split();
  return headNode;
}

function getAllLabelsAndConnects(node, explored, labels, connections) {
  if (explored.includes(node)) {
    return;
  }
  explored.push(node);
  labels.push(node.getDigraphLabel());

  for (const e of node.getDigraphConnections()) {
    connections.push(e);
  }

  for (const child of node.children) {
    getAllLabelsAndConnects(child, explored, labels, connections);
  }
}

function drawTree(root) {
  let graphvizString = "digraph G {\n";
  const labels = [];
  const connections = [];
  const explored = [];

  getAllLabelsAndConnects(root, explored, labels, connections);
  for (const e of labels) {
    graphvizString += e;
  }
  for (const e of connections) {
    graphvizString += e;
  }

  graphvizString += "}";

  return graphvizString.replace(/\n/g, '<br>');
}
  
function generateTree(n, maxSplit) {
  tree = createTree(n, maxSplit, 2)
  return drawTree(tree)
}