class EmptyQueueError(Exception):
    pass


class ArrayQueue:
    def __init__(self, default_size=10):
        self.items = [None] * default_size
        self.front = 0
        self.count = 0

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count

    def enqueue(self, item):
        if self.count == len(self.items):
            self.resize(2*len(self.items))
        i = (self.front + self.count) % len(self.items)
        self.items[i] = item
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueError("Stack is Empty")
        x = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % len(self.items)
        self.count -= 1
        return x

    def peek(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items[self.front]

    def display(self):
        i = self.front
        queue_list = []
        while self.items[i] is not None:
            queue_list.append(self.items[i])
            i = (i + 1) % len(self.items)
            if i == self.front:
                break
        return queue_list

    def resize(self,newsize):
        oldlist = self.items
        self.items = [None] * newsize
        i = self.front
        for j in range(self.count):
            self.items[j] = oldlist[i]
            i = (1+i) % len(oldlist)
        self.front = 0


if __name__ == '__main__':
    myqueue = ArrayQueue(10)
    while True:
        print('1.Display queue')
        print('2.Get queue size')
        print('3.Enqueue')
        print('4.Dequeue')
        print('5.Peek')

        try:
            option = int(input('Enter a choice\n'))
            if option == 1:
                print(myqueue.display())
            elif option == 2:
                print(myqueue.size())
            elif option == 3:
                element = int(input('Enter an element to enqueue '))
                myqueue.enqueue(element)
            elif option == 4:
                print('Dequeued element is: ', myqueue.dequeue())
            elif option == 5:
                print('Element at front is ', myqueue.peek())
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")











