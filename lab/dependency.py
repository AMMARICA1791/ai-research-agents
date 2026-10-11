"""Static, bounded internal Python dependency mapping. No imports are executed."""
from __future__ import annotations

from collections import defaultdict


def analyze_internal_dependencies(files: list[dict]) -> dict:
    python = [x for x in files if x["path"].endswith(".py") and "imports" in x]
    modules = {}
    for item in python:
        path = item["path"]
        name = path[:-3].replace("/", ".")
        if name.endswith(".__init__"):
            name = name[:-9]
        modules[name] = path
    edges = set()
    for item in python:
        origin = item["path"]
        for imported in item.get("import_paths", []):
            destination = modules.get(imported)
            if destination and origin != destination:
                edges.add((origin, destination))
    graph = defaultdict(set)
    for source, target in sorted(edges):
        graph[source].add(target)
    # Tarjan SCC, skip singleton no self edges.
    index, sequence, indices, low, stack, onstack, components = 0, [], {}, {}, [], set(), []
    def visit(node):
        nonlocal index
        indices[node] = index
        low[node] = index
        index += 1
        stack.append(node)
        onstack.add(node)
        for neighbor in sorted(graph[node]):
            if neighbor not in indices:
                visit(neighbor)
                low[node] = min(low[node], low[neighbor])
            elif neighbor in onstack:
                low[node] = min(low[node], indices[neighbor])
        if low[node] == indices[node]:
            comp = []
            while True:
                w = stack.pop()
                onstack.remove(w)
                comp.append(w)
                if w == node:
                    break
            if len(comp) > 1:
                components.append(sorted(comp))
    for node in sorted({x for edge in edges for x in edge}):
        if node not in indices:
            visit(node)
    components.sort()
    return {"internal_edges": [{"from": a, "to": b} for a, b in sorted(edges)][:250],
            "edge_count": len(edges), "cycles": components[:15],
            "module_count": len(modules)}
