from LinkedLists.CircularLinkedList import CircularLinkedList


class EmptyQueueError(Exception):
    pass


class LinkedQueue:
    def __init__(self, initial_elements=None):
        self.items = CircularLinkedList()
        if initial_elements is not None:
            for element in initial_elements:
                self.enqueue(element)

    def is_empty(self):
        return self.items.display_list() == []

    def size(self):
        return len(self.items.display_list())

    def enqueue(self, item):
        self.items.insert_at_end(item)

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.delete_first_node()

    def peek(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.display_list()[0]

    def display(self):
        return self.items.display_list()

    def concatenate(self, queue2):
        self.items.concatenate(queue2.items)
        return self


if __name__ == '__main__':
    myqueue = LinkedQueue()
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











