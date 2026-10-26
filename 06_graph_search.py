"""06_graph_search.py — BFS and DFS over a small graph, plus shortest path.

Demonstrates: breadth-first search (level order, shortest path
in an unweighted graph) versus depth-first search, and parent
tracking to reconstruct the path once the target is found.
Run: python3 06_graph_search.py
"""

from collections import deque

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}


def bfs(graph, start):
    seen, order, queue = {start}, [], deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return order


def dfs(graph, start):
    seen, order = set(), []

    def visit(node):
        seen.add(node)
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in seen:
                visit(neighbour)

    visit(start)
    return order


def shortest_path(graph, start, goal):
    """BFS with parent pointers; returns the path or None."""
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return list(reversed(path))
        for neighbour in graph[node]:
            if neighbour not in parent:
                parent[neighbour] = node
                queue.append(neighbour)
    return None


def main():
    assert bfs(GRAPH, "A") == ["A", "B", "C", "D", "E", "F"]
    assert dfs(GRAPH, "A")[0] == "A" and set(dfs(GRAPH, "A")) == set(GRAPH)
    path = shortest_path(GRAPH, "A", "F")
    assert path == ["A", "C", "F"]
    print(f"PROOF: BFS -> {bfs(GRAPH, 'A')}")
    print(f"PROOF: shortest path A -> F = {path}")


if __name__ == "__main__":
    main()
