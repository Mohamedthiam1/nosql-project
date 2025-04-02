from py2neo import Graph

def connect_to_neo4j():
    """Établit la connexion à Neo4j."""
    return Graph("bolt://localhost:7687", auth=("neo4j", "quinzaine")) 

def execute_query(graph, query, params=None):
    """Exécute une requête Cypher et renvoie les résultats."""
    try:
        result = graph.run(query, parameters=params)
        records = list(result)
        return records if records else "No results found."
    except Exception as e:
        return f"Error executing query: {str(e)}"