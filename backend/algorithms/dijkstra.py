"""
Dijkstra's Shortest Path Algorithm
Finds shortest paths between genres in the music graph
"""

import time
from collections import defaultdict
import heapq

class DijkstraAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.execution_time = 0
        
    def compute_shortest_paths(self):
        """
        Compute shortest paths from all nodes using Dijkstra's algorithm
        Returns dictionary of distances
        """
        start_time = time.time()
        
        nodes = list(self.graph.nodes)
        if not nodes:
            self.execution_time = time.time() - start_time
            return {}
        
        # Use first node as source
        source = nodes[0]
        distances = self._dijkstra(source)
        
        self.execution_time = time.time() - start_time
        return distances
    
    def _dijkstra(self, source):
        """
        Dijkstra's algorithm implementation using min heap
        """
        # Initialize distances
        distances = {node: float('inf') for node in self.graph.nodes}
        distances[source] = 0
        
        # Priority queue: (distance, node)
        pq = [(0, source)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            # Skip if already visited
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            # Check if current distance is outdated
            if current_distance > distances[current_node]:
                continue
            
            # Update distances to neighbors
            for edge in self.graph.get_neighbors(current_node):
                neighbor = edge['to']
                weight = edge['weight']
                distance = current_distance + weight
                
                # If shorter path found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances
    
    def find_shortest_path(self, start, end):
        """
        Find the actual shortest path between two nodes
        Returns path and total distance
        """
        if start not in self.graph.nodes or end not in self.graph.nodes:
            return None, float('inf')
        
        # Modified Dijkstra to track paths
        distances = {node: float('inf') for node in self.graph.nodes}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes}
        
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            # If we reached the end node
            if current_node == end:
                break
            
            if current_distance > distances[current_node]:
                continue
            
            for edge in self.graph.get_neighbors(current_node):
                neighbor = edge['to']
                weight = edge['weight']
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        if path[0] != start:
            return None, float('inf')
        
        return path, distances[end]
    
    def compute_all_pairs_shortest_paths(self):
        """
        Compute shortest paths between all pairs of nodes
        Returns dictionary of dictionaries
        """
        all_paths = {}
        
        for source in self.graph.nodes:
            all_paths[source] = self._dijkstra(source)
        
        return all_paths
    
    def find_most_central_genre(self):
        """
        Find the genre with minimum average distance to all other genres
        (Closeness Centrality)
        """
        if not self.graph.nodes:
            return None
        
        all_distances = self.compute_all_pairs_shortest_paths()
        centrality = {}
        
        for node in self.graph.nodes:
            distances = all_distances[node]
            valid_distances = [d for d in distances.values() if d != float('inf')]
            
            if valid_distances:
                centrality[node] = sum(valid_distances) / len(valid_distances)
            else:
                centrality[node] = float('inf')
        
        # Return genre with minimum average distance
        return min(centrality.items(), key=lambda x: x[1])
    
    def compute_eccentricity(self):
        """
        Compute eccentricity for each node
        (Maximum distance from a node to any other node)
        """
        all_distances = self.compute_all_pairs_shortest_paths()
        eccentricity = {}
        
        for node in self.graph.nodes:
            distances = all_distances[node]
            valid_distances = [d for d in distances.values() if d != float('inf')]
            
            if valid_distances:
                eccentricity[node] = max(valid_distances)
            else:
                eccentricity[node] = float('inf')
        
        return eccentricity
    
    def compute_graph_diameter(self):
        """
        Compute diameter of the graph
        (Maximum eccentricity)
        """
        eccentricity = self.compute_eccentricity()
        valid_eccentricities = [e for e in eccentricity.values() if e != float('inf')]
        
        if valid_eccentricities:
            return max(valid_eccentricities)
        return float('inf')
    
    def compute_graph_radius(self):
        """
        Compute radius of the graph
        (Minimum eccentricity)
        """
        eccentricity = self.compute_eccentricity()
        valid_eccentricities = [e for e in eccentricity.values() if e != float('inf')]
        
        if valid_eccentricities:
            return min(valid_eccentricities)
        return float('inf')
    
    def get_statistics(self):
        """Get statistics about the algorithm execution"""
        return {
            'execution_time': self.execution_time,
            'nodes_processed': len(self.graph.nodes),
            'edges_processed': self.graph.edge_count()
        }