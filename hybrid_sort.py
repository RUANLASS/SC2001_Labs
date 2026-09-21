#complexity writeup
'''
Insertion sort time complexity: it happens on n/s arrays of size s. Worst case complexity is O(s^2) for each.
So, time complexity for insertion sort part: O((n/s) * s^2) = O(ns)

Merge sort time complexity: recursion depth = log(n/s), time complexity of merge = O(n).
So time complexity for merge sort part = O(nlog(n/s))

Hybrid time complexity: O(nlog(n/s) + ns) = O(nlogn) for fixed S. 

Smaller s => merge dominates
Larger s => insertion sort comparisons/swaps dominate

Space complexity = O(n)

'''
import random

def insertion_sort(arr, low, high):
    comparisons = 0
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
    return comparisons


def merge(arr, low, mid, high):
    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]

    comparisons = 0
    i = j = 0
    k = low
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    return comparisons

#combining the two functions, basically merge sort until size goes below s
def hybrid(arr, low, high, s):
    size = high - low + 1
    if size <= s:
        return insertion_sort(arr, low, high)

    mid = (low + high) // 2
    comparisons = hybrid(arr, low, mid, s)
    comparisons += hybrid(arr, mid + 1, high, s)
    comparisons += merge(arr, low, mid, high)
    return comparisons

#main function
def hybrid_merge_insertion_sort(arr, s):
    if len(arr) <= 1:
        return arr, 0
    comparisons = hybrid(arr, 0, len(arr) - 1, s)
    return arr, comparisons

def correctness_test():
    test = [random.randint(1, 1000) for _ in range(20)]
    print("Before:", test)
    _, comp = hybrid_merge_insertion_sort(test, s=5)
    print("After: ", test)
    print("Correctly sorted:", test == sorted(test))
    print("Comparisons: ", comp)

if __name__ == "__main__":
    correctness_test()
    