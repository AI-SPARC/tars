import networkx as nx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import MapEdge, MapLayout, MapNode


class MapService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_map(self, name: str, description: str | None = None) -> MapLayout:
        layout = MapLayout(name=name, description=description)
        self.session.add(layout)
        await self.session.commit()
        await self.session.refresh(layout)
        return layout

    async def add_node(
        self, map_id: str, node_key: str, x: float, y: float, theta: float = 0.0
    ) -> MapNode:
        node = MapNode(map_id=map_id, node_key=node_key, x=x, y=y, theta=theta)
        self.session.add(node)
        await self.session.commit()
        await self.session.refresh(node)
        return node

    async def add_edge(
        self,
        map_id: str,
        edge_key: str,
        from_node_key: str,
        to_node_key: str,
        distance: float,
        bidirectional: bool = False,
    ) -> MapEdge:
        edge = MapEdge(
            map_id=map_id,
            edge_key=edge_key,
            from_node_key=from_node_key,
            to_node_key=to_node_key,
            distance=distance,
            bidirectional=bidirectional,
        )
        self.session.add(edge)
        await self.session.commit()
        await self.session.refresh(edge)
        return edge

    async def route_preview(
        self,
        map_id: str,
        start_node_key: str,
        goal_node_key: str,
    ) -> list[str]:
        edges = (
            await self.session.execute(select(MapEdge).where(MapEdge.map_id == map_id))
        ).scalars()
        graph = nx.DiGraph()
        for edge in edges:
            graph.add_edge(edge.from_node_key, edge.to_node_key, weight=edge.distance)
            if edge.bidirectional:
                graph.add_edge(edge.to_node_key, edge.from_node_key, weight=edge.distance)
        try:
            return list(nx.shortest_path(graph, start_node_key, goal_node_key, weight="weight"))
        except (nx.NetworkXNoPath, nx.NodeNotFound) as exc:
            raise ValueError("No route found") from exc
