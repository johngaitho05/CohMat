class Node:
    def __init__(self,value):
        self.info = value
        self.link = None


class CircularLinkedList:
    def __init__(self, initial_elements=None):
        self.last = None
        if initial_elements is not None:
            for element in initial_elements:
                self.insert_at_end(element)

    def display_list(self):
        if self.last is None:
            return []

        p = self.last.link
        lst = []
        while True:
            lst.append(p.info)
            p = p.link
            if p == self.last.link:
                break
        return lst

    def insert_in_beginning(self, data):
        if self.last is None:
            self.insert_in_empty_list(data)
            return
        temp = Node(data)
        temp.link = self.last.link
        self.last.link = temp

    def insert_in_empty_list(self,data):
        temp = Node(data)
        self.last = temp
        self.last.link = self.last

    def insert_at_end(self, data):
        if self.last is None:
            self.insert_in_empty_list(data)
            return
        temp = Node(data)
        temp.link = self.last.link
        self.last.link = temp
        self.last = temp

    def insert_after(self,data,x):
        p = self.last.link
        while True:
            if p.info == x:
                break
            p = p.link
            if p == self.last.link:
                break
        if p == self.last.link and p.info != x:
            print(x, "nort present in the list")
        else:
            temp = Node(data)
            temp.link = p.link
            p.link = temp
            if p == self.last:
                self.last = temp

    def delete_first_node(self):
        if self.last is None:
            return
        first_element = self.last.link.info
        if self.last.link == self.last:
            self.last = None
            return first_element

        self.last.link = self.last.link.link
        return first_element

    def delete_last_node(self):
        if self.last is None: # list is empty
            return
        if self.last.link == self.last: # list has only one node
            self.last =None
            return

        p = self.last.link
        last_element = self.last.info
        while p.link != self.last:
            p =p.link
        p.link = self.last.link
        self.last = p
        return last_element

    def delete_node(self,x):
        if self.last is None: # list is empty
            return
        if self.last.link == self.last and self.last.info == x: # deletion of only node
            self.last = None
            return
        if self.last.link.info == x: # deletion of first node
            self.delete_first_node()
            return

        p = self.last.link
        while p.link != self.last.link:
            if p.info == x:
                break
            p = p.link

        if p.link == self.last.link:
            print(x, "Not found in the list")
        else:
            p.link = p.link.link
            if self.last.info == x:
                self.last = p

    def concatenate(self, list2):  # appends list2 to the original list1
        if self.last is None:
            self.last = list2.start
            return
        if list2.last is None:
            return
        p = self.last.link
        self.last.link = list2.last.link
        list2.last.link = p
        self.last = list2.last
        return self

if __name__ == '__main__':
    default_values = input('Enter a list of default values(separated '
                           'by commas) or press enter to initialize an empty list: ')
    if default_values != '':
        my_list = CircularLinkedList([int(value) for value in default_values.split(',')])
    else:
        my_list = CircularLinkedList()
    while True:
        print('1.Display list')
        print('2.Insert in the beginning')
        print('3.Insert in the end')
        print('4.Insert after')
        print('5.Delete first node')
        print('6.Delete last node')
        print('7.Delete a specific node')
        print('8.Concatenate')

        try:
            option = int(input("Select an action to be performed: "))

            if option == 1:
                print(my_list.display_list())
            elif option == 2:
                data = int(input("Enter the element to be inserted: "))
                my_list.insert_in_beginning(data)
            elif option == 3:
                data = int(input("Enter the element to be : "))
                my_list.insert_at_end(data)
            elif option == 4:
                data = int(input("Enter the element to be inserted: "))
                x = int(input("enter element after which to insert: "))
                my_list.insert_after(data, x)
            elif option == 5:
                my_list.delete_first_node()
            elif option == 6:
                my_list.delete_last_node()
            elif option == 7:
                x = int(input("Specify the node that you want to delete: "))
                my_list.delete_node(x)
            elif option == 8:
                default_values = input('Enter list2 default values separated by commas'
                                       ' or press enter to initialize an empty list: ')
                if default_values != '':
                    new_list = CircularLinkedList([int(value) for value in default_values.split(',')])
                else:
                    new_list = CircularLinkedList()
                print(my_list.concatenate(new_list))
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid choice!")










