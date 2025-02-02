import unittest
from main import load_graph

from Dijkstra import shortest_route

class DijkstraTestCase(unittest.TestCase):
    def test_dijkstra(self):
        graph = load_graph("graph.json")
        self.assertEqual(shortest_route(graph, "Hoofdingang", "B3.209"),
                         (['Hoofdingang', 'Restaurant', 'Trappenhuis C0.1', 'Trappenhuis C1.1', 'Trappenhuis C2.1', 'Trappenhuis C3.1', 'B3.209'], 104.5))  # add assertion here
    def test_dijkstra_mobility(self):
        graph = load_graph("graph.json")
        self.assertEqual(shortest_route(graph, "Hoofdingang", "B3.209", wheelchair=True),
                         (['Hoofdingang', 'Restaurant', 'Ingang Parkeren', 'Lift D.0', 'Lift D.1', 'Lift D.2', 'Lift D.3', 'Trappenhuis C3.2', 'B3.209'], 121.5))
    def test_dijkstra_emergency(self):
        graph = load_graph("graph.json")
        self.assertEqual(shortest_route(graph, "B3.210", "Nooduitgang B3", emergency=True), (['B3.210', 'Trappenhuis B3.1', 'Nooduitgang B3'], 42))

if __name__ == '__main__':
    unittest.main()
