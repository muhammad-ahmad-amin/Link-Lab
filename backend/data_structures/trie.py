"""
Trie Data Structure - Prefix Tree Implementation
Used for efficient genre search and autocomplete
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None
        self.frequency = 0

class GenreTrie:
    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0
        
    def insert(self, word):
        """Insert a word (genre) into the trie"""
        if not word:
            return
        
        word = word.lower()
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_of_word:
            self.word_count += 1
        
        node.is_end_of_word = True
        node.word = word
        node.frequency += 1
    
    def search(self, word):
        """Search for an exact word in the trie"""
        if not word:
            return False
        
        word = word.lower()
        node = self._find_node(word)
        
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix):
        """Check if any word starts with the given prefix"""
        if not prefix:
            return True
        
        prefix = prefix.lower()
        return self._find_node(prefix) is not None
    
    def search_prefix(self, prefix):
        """Find all words that start with the given prefix"""
        if not prefix:
            return self.get_all_words()
        
        prefix = prefix.lower()
        node = self._find_node(prefix)
        
        if not node:
            return []
        
        results = []
        self._collect_words(node, results)
        return results
    
    def _find_node(self, prefix):
        """Find the node corresponding to a prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _collect_words(self, node, results):
        """Collect all words from a node recursively"""
        if node.is_end_of_word:
            results.append({
                'word': node.word,
                'frequency': node.frequency
            })
        
        for child in node.children.values():
            self._collect_words(child, results)
    
    def get_all_words(self):
        """Get all words in the trie"""
        results = []
        self._collect_words(self.root, results)
        return results
    
    def autocomplete(self, prefix, max_results=10):
        """Get autocomplete suggestions for a prefix"""
        suggestions = self.search_prefix(prefix)
        # Sort by frequency (most common first)
        suggestions.sort(key=lambda x: x['frequency'], reverse=True)
        return suggestions[:max_results]
    
    def delete(self, word):
        """Delete a word from the trie"""
        if not word:
            return False
        
        word = word.lower()
        return self._delete_helper(self.root, word, 0)
    
    def _delete_helper(self, node, word, index):
        """Helper function for deletion"""
        if index == len(word):
            if not node.is_end_of_word:
                return False
            
            node.is_end_of_word = False
            node.word = None
            self.word_count -= 1
            
            # Return True if node has no children
            return len(node.children) == 0
        
        char = word[index]
        if char not in node.children:
            return False
        
        child = node.children[char]
        should_delete = self._delete_helper(child, word, index + 1)
        
        if should_delete:
            del node.children[char]
            # Return True if this node has no children and is not end of another word
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False
    
    def count_words(self):
        """Return the number of words in the trie"""
        return self.word_count
    
    def max_depth(self):
        """Calculate the maximum depth of the trie"""
        return self._max_depth_helper(self.root)
    
    def _max_depth_helper(self, node):
        """Helper function for calculating max depth"""
        if not node.children:
            return 0
        
        return 1 + max(self._max_depth_helper(child) for child in node.children.values())
    
    def count_nodes(self):
        """Count total number of nodes in the trie"""
        return self._count_nodes_helper(self.root)
    
    def _count_nodes_helper(self, node):
        """Helper function for counting nodes"""
        count = 1  # Count current node
        for child in node.children.values():
            count += self._count_nodes_helper(child)
        return count
    
    def longest_common_prefix(self):
        """Find the longest common prefix of all words"""
        if not self.root.children:
            return ""
        
        prefix = []
        node = self.root
        
        while len(node.children) == 1 and not node.is_end_of_word:
            char = list(node.children.keys())[0]
            prefix.append(char)
            node = node.children[char]
        
        return ''.join(prefix)
    
    def clear(self):
        """Clear the trie"""
        self.root = TrieNode()
        self.word_count = 0
    
    def get_statistics(self):
        """Get statistics about the trie"""
        return {
            'total_words': self.word_count,
            'total_nodes': self.count_nodes(),
            'max_depth': self.max_depth(),
            'longest_common_prefix': self.longest_common_prefix()
        }
    
    def __str__(self):
        """String representation of the trie"""
        words = self.get_all_words()
        return f"Trie({self.word_count} words): {', '.join([w['word'] for w in words[:5]])}"
    
    def __repr__(self):
        return self.__str__()