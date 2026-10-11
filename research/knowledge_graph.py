"""Knowledge graph for tracking tool relationships and insights."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set
from uuid import uuid4


@dataclass
class KnowledgeNode:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    node_type: str = "unknown"
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: "")


@dataclass
class KnowledgeEdge:
    source_id: str
    target_id: str
    edge_type: str
    weight: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)


class KnowledgeGraph:
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []

    def add_node(self, node: KnowledgeNode) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: KnowledgeEdge) -> None:
        if edge.source_id in self.nodes and edge.target_id in self.nodes:
            self.edges.append(edge)

    def get_neighbors(self, node_id: str) -> List[KnowledgeNode]:
        neighbor_ids: Set[str] = set()
        for edge in self.edges:
            if edge.source_id == node_id:
                neighbor_ids.add(edge.target_id)
            elif edge.target_id == node_id:
                neighbor_ids.add(edge.source_id)
        return [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes]
