class Node:
    def __init__(self, value, priority):
        self.info = value
        self.link = None
        if priority is None:
            self.priority = self.info
        else:
            self.priority = priority


class SortedLinkedList:

    def __init__(self, initial_elements=None):
        self.start = None
        if initial_elements is not None:
            for element in initial_elements:
                self.insert(element)

    def insert(self, data, data_priority=None):
        temp = Node(data,data_priority)

        if self.start is None or temp.priority < self.start.priority:
            temp.link = self.start
            self.start = temp
            return
        p = self.start
        while p.link is not None and p.link.priority <= temp.priority:
            p = p.link
        temp.link = p.link
        p.link = temp

    def search(self, x):
        if self.start is None:
            return
        p = self.start
        position = 1
        while p is not None and p.info <= x:
            if p.info == x:
                break
            position+=1
            p = p.link
        if p is None or p.info != x:
            return
        else:
            return position

    def delete_first_node(self):
        if self.start is None:
            return
        x = self.start.info
        self.start = self.start.link
        return x

    def delete_node(self, x):
        if self.start is None:
            return
        if self.start.info == x:
            self.delete_first_node()
            return
        p = self.start
        while p.link is not None:
            if p.link.info == x:
                break
            p = p.link
        if p.link is None:
            return
        else:
            p.link = p.link.link

    def display_list(self):
        if self.start is None:
            return []
        p = self.start
        lst = []
        while p is not None:
            lst.append(p.info)
            p = p.link
        return lst


if __name__ == '__main__':
    default_values = input('Enter a list of default values(separated '
                           'by commas) or press enter to initialize an empty list: ')
    if default_values != '':
        my_list = SortedLinkedList([int(value) for value in default_values.split(',')])
    else:
        my_list = SortedLinkedList()

    while True:
        print("1.Dispaly List")
        print("2.Insert")
        print("3.Search for an Element")
        try:
            option = int(input("Enter your choice: "))
            if option == 1:
                print(my_list.display_list())
            elif option == 2:
                data = int(input("Enter the element to be inserted: "))
                my_list.insert(data)
            elif option == 3:
                data = int(input("Enter the element to be searched: "))
                my_list.search(data)
            else:
                print('Invalid option')
            print()
        except ValueError:
            print('Invalid option')







