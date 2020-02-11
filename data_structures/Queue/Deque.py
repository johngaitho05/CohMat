from LinkedLists.CircularLinkedList import CircularLinkedList


class EmptyQueueError(Exception):
    pass


class Deque:
    def __init__(self):
        self.items = CircularLinkedList()

    def is_empty(self):
        return self.items.display_list() == []

    def size(self):
        return len(self.items.display_list())

    def insert_rear(self, item):
        self.items.insert_at_end(item)

    def insert_front(self,item):
        self.items.insert_in_beginning(item)

    def delete_front(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.delete_first_node()

    def delete_rear(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.delete_last_node()

    def first(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.display_list()[0]

    def last(self):
        if self.is_empty():
            raise EmptyQueueError("Queue is Empty")
        return self.items.display_list()[-1]

    def display(self):
        return self.items.display_list()


if __name__ == '__main__':
    deque1 = Deque()
    while True:
        print('1.Display queue')
        print('2.Get deque size')
        print('3.Insert at the front')
        print('4.Insert at the end')
        print('5.Delete from front')
        print('6.Delete from rear')
        print('7.Get front value')
        print('8.Get rear value')

        try:
            option = int(input('Enter a choice\n'))
            if option == 1:
                print(deque1.display())
            elif option == 2:
                print(deque1.size())
            elif option == 3:
                element = int(input('Enter an element to enqueue '))
                deque1.insert_front(element)
            elif option == 4:
                element = int(input('Enter an element to enqueue '))
                deque1.insert_rear(element)
            elif option == 5:
                print("deleted item is: ", deque1.delete_front())
            elif option == 6:
                print("deleted item is: ", deque1.delete_rear())
            elif option == 7:
                print(deque1.first())
            elif option == 8:
                print(deque1.last())
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")











