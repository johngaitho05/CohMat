from Sorting.Sorting import *


def linear_search(search_value, a):
    n = len(a)
    sorted_a = quick_sort(a)
    for i in range(n):
        if sorted_a[i] >= search_value:
            break
    if sorted_a[i] == search_value:
        return i  # returns the index of the element in the sorted list
    else:
        return -1  # unsuccessful search


def binary_search(search_value, a):
    sorted_a = binary_sort(a)
    return _search(sorted_a, 0, len(a) - 1, search_value)


def _search(a, first, last, search_value):
    if (first > last):
        return -1
    mid = (first + last)//2
    if search_value > a[mid]:
        return _search(a, mid + 1, last, search_value)
    elif search_value < a[mid]:
        return _search(a, first, mid - 1, search_value)
    else:
        return mid


if __name__ == '__main__':
    lst1 = [3, 17, 11, 9, 14, 6, 57, 2, 16]
    result1 = linear_search(2, lst1)
    result2 = binary_search(57, lst1)
    print("Linear search:")
    if result1 != -1:
        print("SearchValue found at index", result1)
    else:
        print("SearchValue not found!")
    print("Binary search:")
    if result2 != -1:
        print("SearchValue found at index", result2)
    else:
        print("SearchValue not found!")






