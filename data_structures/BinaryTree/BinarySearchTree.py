from collections import deque


class TreeEmptyError(Exception):
    pass


class Node:
    def __init__(self,value):
        self.info = value
        self.lchild = None
        self.rchild = None


class BinarySearchTree:
    def __init__(self):
        self.root  = None

    def is_empty(self):
        return self.root is None

    def display(self):
        self._display(self.root,0)

    def _display(self,p, level):
        if p is None:
            return
        self._display(p.rchild, level+1)
        print()

        for i in range(level):
            print("   ", end="")
        print(p.info)
        self._display(p.lchild, level+1)

    def insert(self,x):
        self.root = self._insert(self.root, x)

    def _insert(self,p, x):
        if p is None:
            p = Node(x)
        elif x < p.info:
            p.lchild = self._insert(p.lchild, x)
        else:
            p.rchild = self._insert(p.rchild, x)
        return p

    def search(self, x):
        return self._search(self.root, x)

    def _search(self,p, x):
        if p is None:
            return None
        if x < p.info:
            return self._search(p.lchild, x)
        if x > p.info:
            return self._search(p.rchild, x)
        return p

    def delete(self, x):
        self.root = self._delete(self.root, x)

    def _delete(self, p, x):
        if p is None:
            print(x, "not found")
            return p
        if x < p.info: # delete from left subtree
            p.lchild = self._delete(p.lchild, x)
        elif x > p.info: # delete from right subtree
            p.rchild = self._delete(p.rchild, x)
        else:
            # key to be deleted is found
            if p.lchild is not None and p.rchild is not None: # 2 children
                s = p.rchild
                while s.lchild is not None:
                    s = s.lchild
                p.info = s.info
                p.rchild = self._delete(p.rchild, s.info)
            else: # 1 or no child
                if p.lchild is not None: # only left child
                    ch = p.lchild
                else: # only riht child or no child
                    ch = p.rchild
                p = ch
        return p

    def min(self):
        if self.is_empty():
            raise TreeEmptyError("Tree is empty")
        return self._min(self.root).info

    def _min(self,p):
        if p.lchild is None:
            return p
        return self._min(p.lchild)

    def max(self):
        if self.is_empty():
            raise TreeEmptyError("Tree is empty")
        return self._max(self.root).info

    def _max(self, p):
        if p.rchild is None:
            return p
        return self._max(p.rchild)

    def preorder(self):
        return self._preorder(self.root)

    def _preorder(self, p):
        if p is None:
            return []
        elif p.lchild is None and p.rchild is None:
            return [p.info]
        elif p.rchild is None:
            return [p.info] + self._preorder(p.lchild)
        elif p.lchild is None:
            return [p.info] + self._preorder(p.rchild)
        else:
            return [p.info]+ self._preorder(p.lchild) + self._preorder(p.rchild)

    def inorder(self):
        return self._inorder(self.root)

    def _inorder(self,p):
        if p is None:
            return []
        elif p.lchild is None and p.rchild is None:
            return [p.info]
        elif p.rchild is None:
            return self._inorder(p.lchild) + [p.info]
        elif p.lchild is None:
            return [p.info] + self._inorder(p.rchild)
        else:
            return self._inorder(p.lchild) + [p.info] + self._inorder(p.rchild)

    def postorder(self):
        return self._postorder(self.root)

    def _postorder(self, p):
        if p is None:
            return []
        elif p.lchild is None and p.rchild is None:
            return [p.info]
        elif p.rchild is None:
            return self._postorder(p.lchild) + [p.info]
        elif p.lchild is None:
            return self._postorder(p.rchild) + [p.info]
        else:
            return self._postorder(p.lchild) + self._postorder(p.rchild) + [p.info]

    def level_order(self):
        if self.root is None:
            return
        qu = deque()
        qu.append(self.root)
        while len(qu) != 0:
            p = qu.popleft()
            print(p.info + " ", end='')
            if p.lchild is not None:
                qu.append(p.lchild)
            if p.rchild is not None:
                qu.append(p.rchild)

    def height(self):
        return self._height(self.root)

    def _height(self,p):
        if p is None:
            return 0
        hL = self._height(p.lchild)
        hR = self._height(p.rchild)

        if hL > hR:
            return 1 + hL
        else:
            return 1 + hR


###########################################################
if __name__ == '__main__':
    bst = BinarySearchTree()

    while True:
        print("1. Insert an element")
        print("2. Display")
        print("3. Search")
        print("4. Delete")
        print("5. Traverse")
        print("6.Get tree height")
        print("7.Minimum value")
        print("8.Maximum value")

        try:
            option = int(input("Enter your choice\n"))
            if option == 1:
                to_insert = int(input("Enter an element to insert: "))
                bst.insert(to_insert)
            elif option == 2:
                bst.display()
            elif option == 3:
                element = int(input('Enter an element to search: '))
                if bst.search(element):
                    print("Element found")
                else:
                    print("Element not found")
            elif option == 4:
                element = int(input('Enter an element to delete: '))
                bst.delete(element)
            elif option == 5:
                style = int(input("Select traversal method:\n1.Preorder 2.Inorder 3.Postorder\n"))
                if style == 1:
                    print(bst.preorder())
                    print()
                elif style == 2:
                    print(bst.inorder())
                    print()
                elif style == 3:
                    print(bst.postorder())
                    print()
            elif option == 6:
                print("Height of tree is: ", bst.height())
            elif option == 7:
                print(bst.min())
            elif option == 8:
                print(bst.max())
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid option")






