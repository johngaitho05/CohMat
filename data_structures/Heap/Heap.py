class HeapEmptyError(Exception):
    pass


class MaxHeap:
    def __init__(self,maxSize=10, initial_elements=None):
        self.a = [None]*maxSize
        self.n = 0
        if initial_elements is not None:
            for element in initial_elements:
                self.insert(element)

    def insert(self, value):
        self.n+=1
        self.a[self.n] = value
        self.restore_up(self.n)

    def restore_up(self, i):
        k = self.a[i]
        iparent =  i//2

        if type(k) != int:
            while iparent >= 1 and self.a[iparent].priority < k.priority:
                self.a[i] = self.a[iparent]
                i = iparent
                iparent = i//2
        else:
            while iparent >= 1 and self.a[iparent] < k:
                self.a[i] = self.a[iparent]
                i = iparent
                iparent = i//2
        self.a[i] = k

    def delete_root(self):
        if self.n == 0:
            raise HeapEmptyError("Heap is empty")
        maxValue = self.a[1]
        self.a[1] = self.a[self.n]
        self.n-=1
        self.restore_down(1)
        return maxValue

    def restore_down(self, i):
        k = self.a[i]
        lchild = 2*i
        rchild = lchild+1

        if type(k) != int:
            while rchild <= self.n:
                if k.priority >= self.a[lchild].priority and k.priority >= self.a[rchild].priority:
                    self.a[i] = k
                    return
                else:
                    if self.a[lchild].priority > self.a[rchild].priority:
                        self.a[i] = self.a[lchild]
                        i = lchild
                    else:
                        self.a[i] = self.a[rchild]
                        i = rchild
                lchild = 2*i
                rchild = lchild+1

            # if number of nodes is even
            if lchild == self.n and k.priority < self.a[lchild].priority:
                self.a[i] = self.a[lchild]
                i = lchild
            self.a[i] = k
        else:
            while rchild <= self.n:
                if k >= self.a[lchild] and k >= self.a[rchild]:
                    self.a[i] = k
                    return
                else:
                    if self.a[lchild] > self.a[rchild]:
                        self.a[i] = self.a[lchild]
                        i = lchild
                    else:
                        self.a[i] = self.a[rchild]
                        i = rchild
                lchild = 2 * i
                rchild = lchild + 1

            # if number of nodes is even
            if lchild == self.n and k < self.a[lchild]:
                self.a[i] = self.a[lchild]
                i = lchild

            self.a[i] = k

    def display(self):
        if self.n == 0:
            return []
        return self.a[1:self.n+1]


if __name__ == '__main__':
    h = MaxHeap()
    while True:
        print("1.Display")
        print("2.Insert")
        print("3.Delete root")

        try:
            option = int(input("Enter your choice: "))
            if option == 1:
                print(h.display())
            elif option == 2:
                data = int(input("Enter the element to be inserted: "))
                h.insert(data)
            elif option == 3:
                h.delete_root()
            else:
                print('Invalid option')
            print()
        except ValueError:
            print('Invalid option')


















