from BinaryTree.BinarySearchTree import BinarySearchTree
from Heap.Heap import MaxHeap
from Queue.LinkedQueue import LinkedQueue
from LinkedLists.CircularLinkedList import CircularLinkedList

def selection_sort(a):
    for i in range(len(a)-1):
        minIndex = i
        for j in range(i+1, len(a)):
            if a[j] < a[minIndex]:
                minIndex = j
        if i != minIndex:
            a[i],a[minIndex] = a[minIndex],a[i]
    return a


def bubble_sort(a):
    for x in range(len(a)-1, 0,-1):
        swaps = 0
        for j in range(x):
            if a[j] > a[j+1]:
                a[j],a[j+1] = a[j+1],a[j]
                swaps += 1
        if swaps == 0:
            break
    return a


def insertion_sort(a):
    for i in range(1, len(a)):
        temp = a[i]
        j = i-1
        while j >= 0 and a[j]>temp:
            a[j+1] = a[j]
            j = j-1
        a[j+1] = temp
    return a


def shell_sort(a):
    n = len(a)
    h = 1
    while h <= (n-1)/9:
        h = (3*h)+1
    while h >= 1:
        for i in range(h, len(a)):
            temp = a[i]
            j = i-h
            while j >= 0 and a[j] > temp:
                a[j+h] = a[j]
                j = j-h
            a[j+h] = temp
        h = (h-1)/3

    return a


def merge_sort(a):
    n = len(a)
    temp = [None]*n
    return sort(a, temp,0,n-1)


def sort(a, temp, low, up):
    if low == up:
        return

    mid = (low +up) // 2
    sort(a, temp, low, mid)
    sort(a, temp, mid+1, up)
    # merge a[low]...a[mid] and a[mid+1]...a[up] to temp[low]...temp[up]
    merge(a, temp, low, mid, mid+1, up)
    # copy temp[low]....temp[up] to a[low]...a[up]
    copy(a, temp, low, up)
    return a


def merge(a, temp,low1,up1,low2,up2):
    i = low1
    j = low2
    k = low1
    while i <= up1 and j <= up2:
        if a[i] <= a[j]:
            temp[k] = a[i]
            i += 1
        else:
            temp[k] = a[j]
            j += 1
        k += 1
    while i <= up1:
        temp[k] = a[i]
        i += 1
        k += 1
    while j <= up2:
        temp[k] = a[j]
        j += 1
        k += 1


# copies temp[low]...temp[up] to a[low]...a[up]
def copy(a, temp, low, up):
    for i in range(low, up+1):
        a[i] = temp[i]


def quick_sort(a):
    return sort1(a, 0, len(a)-1)


def sort1(a, low, up):
    if low >= up:
        return
    p = partition(a, low, up)
    sort1(a, low, p-1)  # sort left sublist
    sort1(a, p+1, up)  # sort right sublist
    return a


def partition(a,low, up):
    pivot = a[low]
    i = low+1  # moves from left to right
    j = up    # moves from right to left

    while i <= j:
        while a[i] < pivot and i < up:
            i += 1
        while a[j] > pivot:
            j -= 1
        if i < j:  # swap a[i] and a[j]
            temp = a[i]
            a[i] = a[j]
            a[j] = temp
            i += 1
            j -= 1
        else:  # found proper place for pivot
            break
    # proper place for pivot is j
    a[low] = a[j]
    a[j] = pivot

    return j


def binary_sort(a):
    tree = BinarySearchTree()
    for element in a:
        tree.insert(element)
    return tree.inorder()


def heap_sort(a):
    heap = MaxHeap(initial_elements=a)
    index = len(a)-1
    while index >= 0:
        a[index] = heap.delete_root()
        index -= 1
    return a


def radix_sort(a):
    queues = [None] * 10
    mostSigPos = digitsinLargest(a)
    for k in range(1, mostSigPos+1):
        for element in a:
            dig = digit(element, k)
            if queues[dig] is None:
                queues[dig] = LinkedQueue()
            queues[dig].enqueue(element)
        a = concatenate(queues).display()
        queues = [None] * 10
    return a


def concatenate(queues):
    return _concatenate(0, queues)


def _concatenate(n, queues):
    if n == 9:
        if queues[9] is None:
            queues[9] = LinkedQueue()
        return queues[9]
    elif queues[n] is None:
        return _concatenate(n+1, queues)
    return queues[n].concatenate(_concatenate(n+1, queues))


def digitsinLargest(a):
    heap = MaxHeap(initial_elements=a)
    large = heap.delete_root()
    digits = 0
    while large != 0:
        digits = digits+1
        large//=10
    return digits


def digit(n, k):
    d = 0
    for i in range(1,k+1):
        d = n%10
        n//=10
    return d


if __name__ == '__main__':
    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Selection sort:")
    print("Sorted list is:", selection_sort(lst1))

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Bubble sort:")
    print("Sorted list is:", bubble_sort(lst1))

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Insertion Sort:")
    print("Sorted list is:", insertion_sort(lst1))

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Shell Sort:")
    print("Sorted list is:", shell_sort(lst1))

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Merge Sort:")
    print("Sorted list is:", merge_sort(lst1))

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Quick Sort:")
    quick_sort(lst1)
    print("Sorted list is:", lst1)

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Binary Sort:")
    print("Sorted list is:", binary_sort(lst1))

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Heap Sort:")
    print("Sorted list is:", heap_sort(lst1))

    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16, ]
    print("Radix Sort:")
    print("Sorted list is:", radix_sort(lst1))
