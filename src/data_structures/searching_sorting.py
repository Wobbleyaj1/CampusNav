# Searching and sorting algorithms

class Searching:
    def __init__(self):
        """Initialize the searching and sorting module."""
        pass

    def linear_search(self, array, target):
        """Perform a linear search for a target in the array."""
        for index, value in enumerate(array):
            if value == target:
                return index  # Return the index of the target
        return -1  # Return -1 if the target is not found

    def binary_search(self, array, target):
        """Perform a binary search for a target in the sorted array."""
        left, right = 0, len(array) - 1
        while left <= right:
            mid = (left + right) // 2
            if array[mid] == target:
                return mid  # Return the index of the target
            elif array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1  # Return -1 if the target is not found

class Sorting:
    def bubble_sort(self, array):
        """Sort the array using bubble sort."""
        n = len(array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    def selection_sort(self, array):
        """Sort the array using selection sort."""
        n = len(array)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if array[j] < array[min_index]:
                    min_index = j
            array[i], array[min_index] = array[min_index], array[i]
        return array

    def insertion_sort(self, array):
        """Sort the array using insertion sort."""
        for i in range(1, len(array)):
            key = array[i]
            j = i - 1
            while j >= 0 and key < array[j]:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = key
        return array

    def quick_sort(self, array):
        """Sort the array using quick sort."""
        if len(array) <= 1:
            return array
        pivot = array[len(array) // 2]
        left = [x for x in array if x < pivot]
        middle = [x for x in array if x == pivot]
        right = [x for x in array if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)

    def merge_sort(self, array):
        """Sort the array using merge sort."""
        if len(array) <= 1:
            return array
        mid = len(array) // 2
        left = self.merge_sort(array[:mid])
        right = self.merge_sort(array[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        """Helper function to merge two sorted arrays."""
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    