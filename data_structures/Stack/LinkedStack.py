from LinkedLists.SingleLinkedList import SingleLinkedList


class EmptyStackError(Exception):
    pass


class LinkedStack:
    def __init__(self):
        self.items = SingleLinkedList()

    def is_empty(self):
        return self.items.display_list() == []

    def size(self):
        return len(self.items.display_list())

    def push(self, item):
        self.items.insert_in_beginning(item)

    def pop(self):
        if self.is_empty():
            raise EmptyStackError("Stack is Empty")
        return self.items.delete_first_node()

    def peek(self):
        if self.is_empty():
            raise EmptyStackError("Stack is Empty")
        return self.items.display_list()[0]

    def display(self):
        print(self.items.display_list())
        return self.items.display_list()


if __name__ == '__main__':
    st = LinkedStack()
    while True:
        print('1.Display stack')
        print('2.Get stack size')
        print('3.Push')
        print('4.Pop')
        print('5.Peek')

        try:
            option = int(input('Enter a choice\n'))
            if option == 1:
                st.display()
            elif option == 2:
                print(st.size())
            elif option == 3:
                element = int(input('Enter an element to insert: '))
                st.push(element)
            elif option == 4:
                print('Popped element is: ', st.pop())
            elif option == 5:
                print('Topmost element of the stack is: ', st.peek())
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")











