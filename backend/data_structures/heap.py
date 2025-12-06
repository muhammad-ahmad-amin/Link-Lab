"""
Max Heap Data Structure - Priority Queue Implementation
Used for managing recommendation priorities
"""

class RecommendationHeap:
    def __init__(self):
        self.heap = []
        self.genre_map = {}  # Maps genre to index in heap
        
    def insert(self, genre, score):
        """Insert a genre with its recommendation score"""
        item = {'genre': genre, 'score': score}
        self.heap.append(item)
        self.genre_map[genre] = len(self.heap) - 1
        self._heapify_up(len(self.heap) - 1)
    
    def extract_max(self):
        """Remove and return the genre with highest score"""
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            item = self.heap.pop()
            del self.genre_map[item['genre']]
            return item
        
        max_item = self.heap[0]
        del self.genre_map[max_item['genre']]
        
        # Move last element to root
        self.heap[0] = self.heap.pop()
        if self.heap:
            self.genre_map[self.heap[0]['genre']] = 0
            self._heapify_down(0)
        
        return max_item
    
    def peek(self):
        """Return the maximum element without removing it"""
        return self.heap[0] if self.heap else None
    
    def _heapify_up(self, index):
        """Move element up to maintain heap property"""
        while index > 0:
            parent_index = (index - 1) // 2
            
            if self.heap[parent_index]['score'] < self.heap[index]['score']:
                # Swap with parent
                self._swap(parent_index, index)
                index = parent_index
            else:
                break
    
    def _heapify_down(self, index):
        """Move element down to maintain heap property"""
        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2
            
            # Check left child
            if (left < len(self.heap) and 
                self.heap[left]['score'] > self.heap[largest]['score']):
                largest = left
            
            # Check right child
            if (right < len(self.heap) and 
                self.heap[right]['score'] > self.heap[largest]['score']):
                largest = right
            
            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break
    
    def _swap(self, i, j):
        """Swap two elements in the heap"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.genre_map[self.heap[i]['genre']] = i
        self.genre_map[self.heap[j]['genre']] = j
    
    def update_score(self, genre, new_score):
        """Update the score of a genre"""
        if genre not in self.genre_map:
            self.insert(genre, new_score)
            return
        
        index = self.genre_map[genre]
        old_score = self.heap[index]['score']
        self.heap[index]['score'] = new_score
        
        if new_score > old_score:
            self._heapify_up(index)
        else:
            self._heapify_down(index)
    
    def size(self):
        """Return the number of elements in the heap"""
        return len(self.heap)
    
    def is_empty(self):
        """Check if heap is empty"""
        return len(self.heap) == 0
    
    def clear(self):
        """Clear the heap"""
        self.heap.clear()
        self.genre_map.clear()
    
    def get_all_sorted(self):
        """Get all elements in sorted order (non-destructive)"""
        temp_heap = RecommendationHeap()
        
        # FIXED: rebuild heap properly instead of copying invalid genre_map
        for item in self.heap:
            temp_heap.insert(item['genre'], item['score'])
        
        sorted_items = []
        while not temp_heap.is_empty():
            sorted_items.append(temp_heap.extract_max())
        
        return sorted_items
    
    def get_top_k(self, k):
        """Get top k genres by score (non-destructive)"""
        sorted_items = self.get_all_sorted()
        return sorted_items[:k]
    
    def build_heap(self, items):
        """Build heap from list of (genre, score) tuples"""
        self.clear()
        for genre, score in items:
            self.insert(genre, score)
    
    def validate_heap_property(self):
        """Validate that heap property is maintained"""
        for i in range(len(self.heap)):
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < len(self.heap):
                if self.heap[i]['score'] < self.heap[left]['score']:
                    return False
            
            if right < len(self.heap):
                if self.heap[i]['score'] < self.heap[right]['score']:
                    return False
        
        return True
    
    def __str__(self):
        """String representation of the heap"""
        return f"Heap({self.size()} items): {[item['genre'] + ':' + str(item['score']) for item in self.heap]}"

    
    def __repr__(self):
        return self.__str__()
