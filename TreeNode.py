class TreeNode:

    def __init__(self, left=None, right=None, name=None):

        self.left = left
        self.right = right
        self.name = name

    def getLeft(self):

        return self.left

    def getRight(self):

        return self.right

    def getName(self):

        return self.name

    def setLeft(self, left):

        self.left = left

    def setRight(self, right):

        self.right = right

    def setName(self, name):

        self.name = name

    def preorder(self, root):

        if root is None:

            return ""

        print(root.name)
        self.preorder(root.left)
        self.preorder(root.right)

        return ""

