from py2neo import Graph
import os
project_dir = os.path.dirname(os.path.abspath(__file__))

graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="sgxsgwbd"
)
