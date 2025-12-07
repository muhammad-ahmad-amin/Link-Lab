"""
Binary Search Tree Data Structure
Used for managing artists and their song counts
"""

class BSTNode:
    def __init__(self, artist, count):
        self.artist = artist
        self.count = count
        self.left = None
        self.right = None

class ArtistBST:
    def __init__(self):
        self.root = None
        self._size = 0
        
    def insert(self, artist, count):
        """Insert an artist with their song count"""
        if not self.root:
            self.root = BSTNode(artist, count)
            self._size += 1
        else:
            self._insert_helper(self.root, artist, count)
    
    def _insert_helper(self, node, artist, count):
        """Helper function for insertion"""
        # Compare by count (primary) and artist name (secondary)
        if count < node.count or (count == node.count and artist < node.artist):
            if not node.left:
                node.left = BSTNode(artist, count)
                self._size += 1
            else:
                self._insert_helper(node.left, artist, count)
        elif count > node.count or (count == node.count and artist > node.artist):
            if not node.right:
                node.right = BSTNode(artist, count)
                self._size += 1
            else:
                self._insert_helper(node.right, artist, count)
        # If artist already exists, update count
        else:
            node.count = count
    
    def search(self, artist):
        """Search for an artist"""
        return self._search_helper(self.root, artist)
    
    def _search_helper(self, node, artist):
        """Helper function for search"""
        if not node:
            return None
        
        if artist == node.artist:
            return node.count
        
        # Search in both subtrees
        left_result = self._search_helper(node.left, artist)
        if left_result is not None:
            return left_result
        
        return self._search_helper(node.right, artist)
    
    def inorder_traversal(self):
        """Return list of artists in inorder (sorted by count)"""
        result = []
        self._inorder_helper(self.root, result)
        return result
    
    def _inorder_helper(self, node, result):
        """Helper function for inorder traversal"""
        if node:
            self._inorder_helper(node.left, result)
            result.append({'artist': node.artist, 'count': node.count})
            self._inorder_helper(node.right, result)
    
    def preorder_traversal(self):
        """Return list of artists in preorder"""
        result = []
        self._preorder_helper(self.root, result)
        return result
    
    def _preorder_helper(self, node, result):
        """Helper function for preorder traversal"""
        if node:
            result.append({'artist': node.artist, 'count': node.count})
            self._preorder_helper(node.left, result)
            self._preorder_helper(node.right, result)
    
    def postorder_traversal(self):
        """Return list of artists in postorder"""
        result = []
        self._postorder_helper(self.root, result)
        return result
    
    def _postorder_helper(self, node, result):
        """Helper function for postorder traversal"""
        if node:
            self._postorder_helper(node.left, result)
            self._postorder_helper(node.right, result)
            result.append({'artist': node.artist, 'count': node.count})
    
    def range_query(self, min_count, max_count):
        """Find all artists with song count in range [min_count, max_count]"""
        result = []
        self._range_query_helper(self.root, min_count, max_count, result)
        return result
    
    def _range_query_helper(self, node, min_count, max_count, result):
        """Helper function for range query"""
        if not node:
            return
        
        # If current node's count is in range
        if min_count <= node.count <= max_count:
            result.append({'artist': node.artist, 'count': node.count})
        
        # Recursively check both subtrees
        if node.count >= min_count:
            self._range_query_helper(node.left, min_count, max_count, result)
        if node.count <= max_count:
            self._range_query_helper(node.right, min_count, max_count, result)
    
    def find_min(self):
        """Find artist with minimum song count"""
        if not self.root:
            return None
        
        node = self.root
        while node.left:
            node = node.left
        
        return {'artist': node.artist, 'count': node.count}
    
    def find_max(self):
        """Find artist with maximum song count"""
        if not self.root:
            return None
        
        node = self.root
        while node.right:
            node = node.right
        
        return {'artist': node.artist, 'count': node.count}
    
    def height(self):
        """Calculate the height of the tree"""
        return self._height_helper(self.root)
    
    def _height_helper(self, node):
        """Helper function for calculating height"""
        if not node:
            return -1
        
        left_height = self._height_helper(node.left)
        right_height = self._height_helper(node.right)
        
        return 1 + max(left_height, right_height)
    
    def size(self):
        """Return the number of nodes in the tree"""
        return self._size
    
    def is_empty(self):
        """Check if tree is empty"""
        return self.root is None
    
    def level_order_traversal(self):
        """Return list of artists in level order (BFS)"""
        if not self.root:
            return []
        
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append({'artist': node.artist, 'count': node.count})
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    def count_leaves(self):
        """Count the number of leaf nodes"""
        return self._count_leaves_helper(self.root)
    
    def _count_leaves_helper(self, node):
        """Helper function for counting leaves"""
        if not node:
            return 0
        if not node.left and not node.right:
            return 1
        return self._count_leaves_helper(node.left) + self._count_leaves_helper(node.right)
    
    def is_balanced(self):
        """Check if the tree is balanced"""
        return self._is_balanced_helper(self.root)[0]
    
    def _is_balanced_helper(self, node):
        """Helper function for checking balance"""
        if not node:
            return True, -1
        
        left_balanced, left_height = self._is_balanced_helper(node.left)
        if not left_balanced:
            return False, 0
        
        right_balanced, right_height = self._is_balanced_helper(node.right)
        if not right_balanced:
            return False, 0
        
        balanced = abs(left_height - right_height) <= 1
        height = 1 + max(left_height, right_height)
        
        return balanced, height
    
    def clear(self):
        """Clear the tree"""
        self.root = None
        self._size = 0
    
    def get_statistics(self):
        """Get statistics about the BST"""
        return {
            'size': self._size,
            'height': self.height(),
            'leaf_count': self.count_leaves(),
            'is_balanced': self.is_balanced(),
            'min': self.find_min(),
            'max': self.find_max()
        }
    
    def __str__(self):
        """String representation of the BST"""
        artists = self.inorder_traversal()[:5]
        return f"BST({self._size} artists): {', '.join([a['artist'] for a in artists])}"
    
    def __repr__(self):
        return self.__str__()