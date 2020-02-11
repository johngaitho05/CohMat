class EmptyStackError(Exception):
    pass


class ArrayStack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise EmptyStackError("Stack is Empty")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise EmptyStackError("Stack is Empty")
        return self.items[-1]

    def display(self):
        print(self.items)
        return self.items


if __name__ == '__main__':
    st = ArrayStack()
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
                element = input('Enter an element to insert: ')
                st.push(element)
            elif option == 4:
                print('Popped element is: ', st.pop())
            elif option == 5:
                print('Last element of the stack is: ', st.peek())
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")











