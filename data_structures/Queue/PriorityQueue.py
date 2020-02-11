from Heap.Heap import MaxHeap


class EmptyQueueError(Exception):
    pass


class Node:
    def __init__(self, data, priority):
        self.info = data
        self.priority = priority


class PriorityQueue:
    def __init__(self):
        self.items = MaxHeap()

    def is_empty(self):
        return self.items.display() == []

    def size(self):
        return len(self.items.display())

    def enqueue(self, data,data_priority):
        temp = Node(data, data_priority)
        self.items.insert(temp)

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.delete_root().info

    def peek(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.display()[0].info

    def display(self):
        return [item.info for item in self.items.display()]


if __name__ == '__main__':
    myqueue = PriorityQueue()
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
                element = int(input('Enter an element to enqueue: '))
                element_priority = int(input("Enter a value to represent the element's priority: "))
                myqueue.enqueue(element,element_priority)
            elif option == 4:
                print('Dequeued element is: ', myqueue.dequeue())
            elif option == 5:
                print('Element at front is ', myqueue.peek())
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")











