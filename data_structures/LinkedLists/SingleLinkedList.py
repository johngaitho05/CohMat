class InvalidOperationException(Exception):
    pass


class Node:
    def __init__(self, value):
        self.info = value
        self.link = None


def _merge(p1, p2):
    if p1.info <= p2.info:
        startM = Node(p1.info)
        p1 = p1.link
    else:
        startM = Node(p2.info)
        p2 = p2.link
    pM = startM

    while p1 is not None and p2 is not None:
        if p1.info <= p2.info:
            pM.link = p1
            p1 = p1.link
        else:
            pM.link = p2
            p2 = p2.link
        pM = pM.link

    if p1 is None:
        pM.link = p2
    else:
        pM.link = p1

    return startM


def _merge1(p1, p2):
    if p1.info <= p2.info:
        startM = Node(p1.info)
        p1 = p1.link
    else:
        startM = Node(p2.info)
        p2 = p2.link
    pM = startM

    while p1 is not None and p2 is not None:
        if p1.info <= p2.info:
            pM.link = Node(p1.info)
            p1 = p1.link
        else:
            pM.link = Node(p2.info)
            p2 = p2.link
        pM = pM.link

    # second list has finished and there are elements remaining in the first list
    while p1 is not None:
        pM.link = Node(p1.info)
        p1 = p1.link
        pM = pM.link

    # first list has finished and there are elements remaining in the second list
    while p2 is not None:
        pM.link = Node(p2.info)
        p2 = p2.link
        pM = pM.link

    return startM


def divide_list(p):
    q = p.link.link
    while q is not None and q.link is not None:
        p = p.link
        q = q.link.link
    start2 = p.link
    p.link = None
    return start2


class SingleLinkedList:
    def __init__(self, initial_elements=None):
        self.start = None
        if initial_elements is not None:
            for element in initial_elements:
                self.insert_at_end(element)

    def display_list(self):
        if self.start is None:
            return []
        else:
            p = self.start
            lst = []
            while p is not None:
                lst.append(p.info)
                p = p.link
            return lst

    def count_nodes(self):
        p = self.start
        n = 0
        while p is not None:
            n += 1
            p = p.link
        return n

    def search(self, x):
        position = 1
        p = self.start
        while p is not None:
            if p.info == x:
                return position
            position += 1
            p = p.link
        else:
            return

    def insert_in_beginning(self, data):
        temp = Node(data)
        temp.link = self.start
        self.start = temp

    def insert_at_end(self, data):
        temp = Node(data)
        if self.start is None:
            self.start = temp
            return
        p = self.start
        while p.link is not None:
            p = p.link
        p.link = temp

    def insert_after(self, data, x):
        p = self.start
        while p is not None:
            if p.info == x:
                break
            p = p.link
        if p is None:
            print(x, "is not in the list")
        else:
            temp = Node(data)
            temp.link = p.link
            p.link = temp

    def insert_before(self, data, x):
        if self.start is None:
            print("List is empty")
            return
        if x == self.start.info:
            self.insert_in_beginning(data)
            return
        p = self.start
        while p.link is not None:
            if p.link.info == x:
                break
            p = p.link
        if p.link is None:
            return
        else:
            temp = Node(data)
            temp.link = p.link
            p.link = temp

    def insert_at_position(self, data, k):
        if k == 1:
            self.insert_in_beginning(data)
            return
        p = self.start
        i = 1
        while i<k-1 and p is not None:
            p = p.link
            i+=1
        if p is None:
            raise InvalidOperationException("Index out of range: You can only insert up to position", i)
        else:
            temp = Node(data)
            temp.link = p.link
            p.link = temp

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

    def delete_first_node(self):
        if self.start is None:
            return
        p = self.start
        self.start = self.start.link
        return p.info

    def delete_last_node(self):
        if self.start is None:
            return
        if self.start.link is None:
            self.start = None
            return
        p = self.start
        while p.link.link is not None:
            p = p.link
        p.link = None

    def reverse_list(self):
        prev = None
        p = self.start
        while p is not None:
            next = p.link
            p.link = prev
            prev = p
            p = next
        self.start = prev

    def bubble_sort_exdata(self):
        end = None
        while self.start.link != end:
            p = self.start
            while p.link != end:
                q = p.link
                if p.info > q.info:
                    p.info, q.info = q.info, p.info
                p = q
            end = p

    def bubble_sort_exlinks(self):
        end = None
        while self.start.link != end:
            r = p = self.start
            while p.link != end:
                q = p.link
                if p.info > q.info:
                    p.link = q.link
                    q.link = p
                    if p != self.start:
                        r.link = q
                    else:
                        self.start = q
                    p, q = q, p
                r = p
                p = p.link
            end = p

    def has_cycle(self):
        if self.find_cycle() is None:
            return False
        else:
            return True

    def find_cycle(self):
        if self.start is None or self.start.link is None:
            return False
        slowR = fastR = self.start
        while slowR is not None and fastR is not None:
            slowR = slowR.link
            fastR = fastR.link.link
            if slowR == fastR:
                return slowR
        return None

    def remove_cycle(self):
        c = self.find_cycle()
        if c is None:
            return
        p = c
        q = c
        len_cycle = 0
        while True:
            len_cycle += 1
            q = q.link
            if p == q:
                break
        len_rem_list = 0
        p = self.start
        while p != q:
            len_rem_list += 1
            p = p.link
            q = q.link
        length_list = len_cycle + len_rem_list
        p = self.start
        for i in range(length_list-1):
            p = p.link
        p.link = None

    def insert_cycle(self, x):
        if self.start is None:
            return
        p = self.start
        px = None
        prev = None
        while p is not None:
            if p.info == x:
                px = p
            prev = p
            p = p.link
        if px is not None:
            prev.link = px
        else:
            return

    # merge by re-arranging links
    def merge(self, list2):
        merge_list = SingleLinkedList()
        merge_list.start = _merge(self.start, list2.start)
        return merge_list

    # merge by creating new list
    def merge1(self,list2):
        merge_list = SingleLinkedList()
        merge_list.start = _merge1(self.start, list2.start)
        return merge_list

    def merge_sort(self):
        self.start = self._merge_sort_rec(self.start)

    # recursive merge sort
    def _merge_sort_rec(self, list_start):
        if list_start is None or list_start.link is None:
            return list_start

        start1 = list_start
        start2 = divide_list(list_start)
        start1 = self._merge_sort_rec(start1)
        start2 = self._merge_sort_rec(start2)
        startM = _merge(start1, start2)
        return startM

    def concatenate(self, list2):  # appends list2 to the original list1
        if self.start is None:
            self.start = list2.start
            return
        if list2.start is None:
            return
        p = self.start
        while p.link is not None:
            p = p.link
        p.link = list2.start


if __name__ == '__main__':
    default_values = input('Enter a list of default values(separated '
                           'by commas) or press enter to initialize an empty list: ')
    if default_values != '':
        my_list = SingleLinkedList([int(value) for value in default_values.split(',')])
    else:
        my_list = SingleLinkedList()
    while True:
        print("1.Display List")
        print("2.Count the number of nodes")
        print("3.Search for an element")
        print("4.Insert in an empty list/insert in beginning")
        print("5.Insert a node at the end of the list")
        print("6.insert a node after a specified node")
        print("7.Insert a node before a specified node")
        print("8.insert a node at a given position")
        print("9.delete first node")
        print("10.Delete last node")
        print("11.delete any node")
        print("12.reverse the list")
        print("13.Bubble sort by exchanging data")
        print("14.Bubble sort by exchanging links")
        print("15.MergeSort")
        print("16.Insert Cycle")
        print("17.Detect Cycle")
        print("18.remove Cycle")
        print("19.Quit")

        option = int(input('Enter your choice: '))
        if option == 1:
            print(my_list.display_list())
        elif option == 2:
            my_list.count_nodes()
        elif option == 3:
            user_data = int(input("Enter the element to be searched: "))
            position = my_list.search(user_data)
            if position is not None:
                print("Element found at position", my_list.search(user_data))
            else:
                print("Element not found")
        elif option == 4:
            user_data = int(input("Enter the element to be inserted: "))
            my_list.insert_in_beginning(user_data)
        elif option == 5:
            user_data = int(input("Enter the element to be inserted: "))
            my_list.insert_at_end(user_data)
        elif option == 6:
            user_data = int(input("Enter the element to be inserted: "))
            x1 = int(input("Enter the element after which to insert: "))
            my_list.insert_after(user_data, x1)
        elif option == 7:
            user_data = int(input("Enter the element to be inserted: "))
            x1 = int(input("Enter the element before which to insert: "))
            my_list.insert_before(user_data, x1)

        elif option == 8:
            user_data = int(input("Enter the element to be inserted: "))
            k1 = int(input("Enter the position at which to insert: "))
            my_list.insert_at_position(user_data, k1)
        elif option == 9:
            my_list.delete_first_node()
        elif option == 10:
            my_list.delete_last_node()
        elif option == 11:
            user_data = int(input("Enter the element to be deleted: "))
            my_list.delete_node(user_data)
        elif option == 12:
            my_list.reverse_list()
        elif option == 13:
            my_list.bubble_sort_exdata()
        elif option == 14:
            my_list.bubble_sort_exlinks()
        elif option == 15:
            my_list.merge_sort()
        elif option == 16:
            user_data = int(input("Enter the element at which the cycle has to be to be inserted: "))
            my_list.insert_cycle(user_data)
        elif option == 17:
            if my_list.has_cycle():
                print("List has cycle")
            else:
                print("List do not have a cycle")
        elif option == 18:
            my_list.remove_cycle()
        elif option == 19:
            break
        else:
            print("Invalid choice!")
        print()
