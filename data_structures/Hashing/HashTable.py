from LinkedLists.SortedLinkedList import SortedLinkedList


class InvalidOperationException(Exception):
    pass


# separate chaining implementation of hash table
class HashTable:
    def __init__(self, tableSize, initial_elements=None):
        self.m = tableSize
        self.array = [None] * self.m
        self.n = 0

        if initial_elements is not None:
            for element in initial_elements:
                self.insert(element)

    # hashing (converting the key in to a memory address)
    def hash(self, key):
        return key % self.m

    def display_table(self):
        for i in range(self.m):
            print("[",i, "] --> ",end='')
            if self.array[i] is not None:
                print(self.array[i].display_list())
            else:
                print("___")

    def search(self,key):
        h = self.hash(key)
        if self.array[h] is None:
            return
        return self.array[h].search(key)

    def insert(self, newRecord):
        h = self.hash(newRecord)
        if self.array[h] is None:
            self.array[h] = SortedLinkedList()
        else:
            if self.search(newRecord) is not None:
                raise InvalidOperationException("The key you tried to insert already exists in the hash table")
        self.array[h].insert(newRecord)
        self.n += 1

    def delete(self, key):
        h = self.hash(key)
        if self.array[h] is None:
            return
        self.array[h].delete_node(key)
        self.n -= 1

    def number_of_records(self):
        return self.n


if __name__ == '__main__':
    table_size = int(input("Enter the hash table size: "))
    default_values = input('Enter a list of default values(separated '
                           'by commas) or press enter to initialize an empty Hash Table: ')
    if default_values != '':
        ht = HashTable(table_size,[int(value) for value in default_values.split(',')])
    else:
        ht = HashTable(table_size)
    while True:
        print("1.Display table")
        print("2.Insert an element")
        print("3.Search an element")
        print("4.Delete an element")
        print("5.Get number of records")

        choice = int(input("Enter your choice:\n"))
        if choice == 1:
            ht.display_table()
        elif choice == 2:
            item = int(input("Enter an element to insert: "))
            ht.insert(item)
        elif choice == 3:
            item = int(input("Enter the element to be searched: "))
            if ht.search(item) is None:
                print("Item not found")
            else:
                print("Element found")
        elif choice == 4:
            item = int(input("Enter an element to delete: "))
            ht.delete(item)
        elif choice  == 5:
            print(ht.number_of_records())
        else:
            print("Invalid option. Try again")


