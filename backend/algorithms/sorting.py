"""
Sorting Algorithms - QuickSort and MergeSort
Used for sorting genres by various criteria
"""

import time

class QuickSort:
    def __init__(self):
        self.comparison_count = 0
        self.execution_time = 0
        
    def sort_by_score(self, genre_scores):
        """
        Sort genres by their recommendation scores (descending)
        Returns sorted list of genre names
        """
        start_time = time.time()
        self.comparison_count = 0
        
        # Convert to list of tuples
        items = [(genre, score) for genre, score in genre_scores.items()]
        
        # Sort using quicksort
        sorted_items = self._quicksort(items, 0, len(items) - 1)
        
        self.execution_time = time.time() - start_time
        
        # Return just the genre names
        return [item[0] for item in sorted_items]
    
    def _quicksort(self, arr, low, high):
        """QuickSort implementation"""
        if low < high:
            # Partition the array
            pi = self._partition(arr, low, high)
            
            # Recursively sort elements before and after partition
            self._quicksort(arr, low, pi - 1)
            self._quicksort(arr, pi + 1, high)
        
        return arr
    
    def _partition(self, arr, low, high):
        """Partition function for QuickSort"""
        # Choose rightmost element as pivot
        pivot = arr[high][1]  # Score value
        i = low - 1
        
        for j in range(low, high):
            self.comparison_count += 1
            
            # Sort in descending order (higher scores first)
            if arr[j][1] >= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def sort_by_name(self, genres):
        """Sort genres alphabetically"""
        start_time = time.time()
        self.comparison_count = 0
        
        sorted_genres = self._quicksort_strings(genres.copy(), 0, len(genres) - 1)
        
        self.execution_time = time.time() - start_time
        return sorted_genres
    
    def _quicksort_strings(self, arr, low, high):
        """QuickSort for strings"""
        if low < high:
            pi = self._partition_strings(arr, low, high)
            self._quicksort_strings(arr, low, pi - 1)
            self._quicksort_strings(arr, pi + 1, high)
        return arr
    
    def _partition_strings(self, arr, low, high):
        """Partition for string sorting"""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            self.comparison_count += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


class MergeSort:
    def __init__(self):
        self.comparison_count = 0
        self.execution_time = 0
        
    def sort_by_distance(self, distances):
        """
        Sort genres by their distances (ascending)
        Returns sorted list of genre names
        """
        start_time = time.time()
        self.comparison_count = 0
        
        # Convert to list of tuples
        items = [(genre, dist) for genre, dist in distances.items()]
        
        # Sort using mergesort
        sorted_items = self._mergesort(items)
        
        self.execution_time = time.time() - start_time
        
        # Return just the genre names
        return [item[0] for item in sorted_items]
    
    def _mergesort(self, arr):
        """MergeSort implementation"""
        if len(arr) <= 1:
            return arr
        
        # Divide array into two halves
        mid = len(arr) // 2
        left = self._mergesort(arr[:mid])
        right = self._mergesort(arr[mid:])
        
        # Merge the sorted halves
        return self._merge(left, right)
    
    def _merge(self, left, right):
        """Merge two sorted arrays"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            self.comparison_count += 1
            
            # Sort by distance (ascending)
            if left[i][1] <= right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Append remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    def sort_by_count(self, genre_counts):
        """
        Sort genres by their frequency counts (descending)
        Returns sorted list of genre names
        """
        start_time = time.time()
        self.comparison_count = 0
        
        items = [(genre, count) for genre, count in genre_counts.items()]
        sorted_items = self._mergesort_descending(items)
        
        self.execution_time = time.time() - start_time
        return [item[0] for item in sorted_items]
    
    def _mergesort_descending(self, arr):
        """MergeSort for descending order"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._mergesort_descending(arr[:mid])
        right = self._mergesort_descending(arr[mid:])
        
        return self._merge_descending(left, right)
    
    def _merge_descending(self, left, right):
        """Merge for descending order"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            self.comparison_count += 1
            
            if left[i][1] >= right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    def sort_artists(self, artist_data):
        """Sort artists by song count"""
        start_time = time.time()
        self.comparison_count = 0
        
        items = [(artist, count) for artist, count in artist_data.items()]
        sorted_items = self._mergesort_descending(items)
        
        self.execution_time = time.time() - start_time
        return dict(sorted_items)


class HeapSort:
    """Heap Sort implementation for comparison"""
    def __init__(self):
        self.comparison_count = 0
        self.execution_time = 0
    
    def sort(self, arr):
        """Sort array using heap sort"""
        start_time = time.time()
        self.comparison_count = 0
        
        n = len(arr)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify(arr, i, 0)
        
        self.execution_time = time.time() - start_time
        return arr
    
    def _heapify(self, arr, n, i):
        """Heapify subtree rooted at index i"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            self.comparison_count += 1
            if arr[left] > arr[largest]:
                largest = left
        
        if right < n:
            self.comparison_count += 1
            if arr[right] > arr[largest]:
                largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest)


def compare_sorting_algorithms(data):
    """
    Compare performance of different sorting algorithms
    """
    import copy
    
    # QuickSort
    qs = QuickSort()
    qs_data = copy.deepcopy(data)
    qs_result = qs.sort_by_score(qs_data)
    
    # MergeSort
    ms = MergeSort()
    ms_data = copy.deepcopy(data)
    ms_result = ms.sort_by_distance(ms_data)
    
    # HeapSort
    hs = HeapSort()
    hs_data = list(data.values())
    hs_result = hs.sort(hs_data)
    
    return {
        'quicksort': {
            'time': qs.execution_time,
            'comparisons': qs.comparison_count,
            'result': qs_result
        },
        'mergesort': {
            'time': ms.execution_time,
            'comparisons': ms.comparison_count,
            'result': ms_result
        },
        'heapsort': {
            'time': hs.execution_time,
            'comparisons': hs.comparison_count,
            'result': hs_result
        }
    }