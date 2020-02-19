"""Data structures and algorithms."""


class Graph:
    """Undirected graph. Adjacency-list implementation."""

    class Node:
        def __init__(self, data, neighbors=[]):
            self.data = data

        def __repr__(self):
            return f"Node({self.data})"

    def __init__(self):
        self.nodes = dict()
        self.node_neighbors = dict()

    def add_node(self, label, data):
        self.nodes[label] = Graph.Node(data)
        self.node_neighbors[label] = []

    def add_edge(self, src_label, dest_label, twoway=True):
        try:
            src_node = self.nodes[src_label]
            dest_node = self.nodes[dest_label]
        except KeyError:
            raise TypeError("Src ({}) and dest ({}) nodes should exist!"
                            .format(src_label, dest_label))

        self.node_neighbors[src_label].append(dest_node)
        if twoway:
            self.node_neighbors[dest_label].append(src_node)

    def __repr__(self):
        repr_format = "{0}: {1} -> {2}"
        return "\n".join(repr_format.format(label,
                                            self.nodes[label],
                                            self.node_neighbors[label])
                         for label in self.nodes.keys())
