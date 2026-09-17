def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr, low, mid, high):
    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]

    i = j = 0
    k = low
    while i < len(left) and j < len(right):
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

#combining the two functions, basically merge sort until size goes below s
def hybrid(arr, low, high, s):
    size = high - low + 1
    if size <= s:
        insertion_sort(arr, low, high)
        return

    mid = (low + high) // 2
    hybrid(arr, low, mid, s)
    hybrid(arr, mid + 1, high, s)
    merge(arr, low, mid, high)

#main function
def hybrid_merge_insertion_sort(arr, s):
    if len(arr) <= 1:
        return arr
    hybrid(arr, 0, len(arr) - 1, s)
    return arr

#complexity writeup
'''
Insertion sort time complexity: it happens on n/s arrays of size s. Worst case complexity is O(s^2) for each.
So, time complexity for insertion sort part: O((n/s) * s^2) = O(ns) = O(n).

Merge sort time complexity: recursion depth = log(n/s), time complexity of merge = O(n).
So time complexity for merge sort part = O(nlog(n/s)) = O(nlogn)

Hybrid time complexity: O(nlog(n/s) + ns) = O(nlogn)

Smaller s => merge dominates
Larger s => insertion sort comparisons/swaps dominate

Space complexity = O(n)

'''