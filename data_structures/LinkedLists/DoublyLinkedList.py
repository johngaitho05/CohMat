class Node:
    def __init__(self, value):
        self.info = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self, initial_elements=None):
        self.start = None
        if initial_elements is not None:
            for element in initial_elements:
                self.insert_at_end(element)

    def display_list(self):
        if self.start is None:
            print("List is empty")
            return []
        else:
            p = self.start
            lst = []
            while p is not None:
                lst.append(p.info)
                p = p.next
            print(lst)
            return lst

    def insert_in_beginning(self, data):
        temp = Node(data)
        temp.next = self.start
        self.start.prev = temp
        self.start = temp

    def insert_in_empty_list(self, data):
        temp = Node(data)
        self.start = temp

    def insert_at_end(self, data):
        if self.start is None:
            self.insert_in_empty_list(data)
            return
        temp = Node(data)
        p = self.start
        while p.next is not None:
            p = p.next
        p.next = temp
        temp.prev = p

    def insert_after(self, data, x):
        temp = Node(data)
        p = self.start
        while p is not None:
            if p.info == x:
                break
            p = p.next

        if p is None:
            print(x, "not present in the list")
        else:
            temp.prev = p
            temp.next = p.next
            if p.next is not None:
                p.next.prev = temp
            p.next = temp

    def insert_before(self, data, x):
        if self.start is None:
            print("List is empty")
            return
        if self.start.info == x:
            self.insert_in_beginning(data)
            return
        p = self.start
        while p is not None:
            if p.info == x:
                break
            p = p.next

        if p is None:
            print(x, "not present in the list")
        else:
            temp = Node(data)
            temp.prev = p.prev
            temp.next = p
            p.prev.next = temp
            p.prev = temp

    def delete_first_node(self):
        if self.start is None:
            return
        if self.start.next is None:
            self.start = None
            return
        self.start = self.start.next
        self.start.prev = None

    def delete_last_node(self):
        if self.start is None:
            return
        if self.start.next is None:
            self.start = None
            return
        p = self.start
        while p.next is not None:
            p = p.next
        p.prev.next = None

    def delete_node(self, x):
        if self.start is None:
            return
        if self.start.next is None:
            if self.start.info == x:
                self.start = None
            else:
                print(x, 'not found')
            return
        if self.start.info == x:
            self.start = self.start.next
            self.start.prev = None
            return
        p = self.start.next
        while p.next is not None:
            if p.info == x:
                break
            p = p.next
        if p.next is not None:
            p.prev.next = p.next
            p.next.prev = p.prev
        else:
            if p.info == x:
                p.prev.next = None
            else:
                print(x, 'not found')

    def reverse_list(self):
        if self.start is None:
            return
        p1 = self.start
        p2 = p1.next
        p1.next = None
        p1.prev = p2
        while p2 is not None:
            p2.prev = p2.next
            p2.next = p1
            p1 = p2
            p2 = p2.prev
        self.start = p1


if __name__ == '__main__':
    default_values = input('Enter a list of default values(separated '
                           'by commas) or press enter to initialize an empty list: ')
    if default_values != '':
        my_list = DoublyLinkedList([int(value) for value in default_values.split(',')])
    else:
        my_list = DoublyLinkedList()
    while True:
        print('1.Display list')
        print('2.Insert in the beginning')
        print('3.Insert in the end')
        print('4.Insert before')
        print('5.Insert after')
        print('6.Delete first node')
        print('7.Delete last node')
        print('8.Delete a specific node')
        print('9.Reverse list')

        try:
            option = int(input("Select an action to be performed: "))

            if option == 1:
                my_list.display_list()
            elif option == 2:
                data = int(input("Enter the element to be inserted: "))
                my_list.insert_in_beginning(data)
            elif option == 3:
                data = int(input("Enter the element to be : "))
                my_list.insert_at_end(data)
            elif option == 4:
                data = int(input("Enter the element to be inserted: "))
                x = int(input("enter element before which to insert: "))
                my_list.insert_before(data, x)
            elif option == 5:
                data = int(input("Enter the element to be inserted: "))
                x = int(input("enter element after which to insert: "))
                my_list.insert_after(data, x)
            elif option == 6:
                my_list.delete_first_node()
            elif option == 7:
                my_list.delete_last_node()
            elif option == 8:
                x = int(input("Specify the node that you want to delete: "))
                my_list.delete_node(x)
            elif option == 9:
                my_list.reverse_list()
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid choice!")
