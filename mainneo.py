from py2neo import Graph

# Connexion à Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "quinzaine"))

def execute_query(query, params=None):
    """Exécute une requête Cypher et affiche les résultats"""
    try:
        result = graph.run(query, parameters=params)
        records = list(result)
        return records if records else "No results found."
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Requêtes Questions 14 à 30
questions_queries = {
    "14. Acteur avec le plus de films": """
        MATCH (a:Actor)-[:A_JOUER]->(m:Film)
        RETURN a.name AS acteur, COUNT(m) AS nombre_de_films
        ORDER BY nombre_de_films DESC
        LIMIT 1
    """,
    "15. Acteurs ayant joué avec Anne Hathaway": """
        MATCH (a:Actor)-[:A_JOUER]->(m:Film)<-[:A_JOUER]-(co_actor:Actor)
        WHERE a.name = 'Anne Hathaway' AND co_actor.name <> 'Anne Hathaway'
        RETURN DISTINCT co_actor.name AS acteur
    """,
    "16. Acteur avec le plus de revenus": """
        MATCH (a:Actor)-[:A_JOUER]->(m:Film)
        RETURN a.name AS acteur, SUM(m.revenue) AS total_revenus
        ORDER BY total_revenus DESC
        LIMIT 1
    """,
    "17. Moyenne des votes": """
        MATCH (m:Film)
        WHERE m.rating IN ['G', 'PG', 'PG-13', 'R', 'NC-17']  
        RETURN AVG(CASE WHEN m.rating = 'G' THEN 1 WHEN m.rating = 'PG' THEN 2 WHEN m.rating = 'PG-13' THEN 3 WHEN m.rating = 'R' THEN 4 ELSE 5 END) AS moyenne_votes
    """,
    "18. Genre le plus représenté": """
        MATCH (m:Film)-[:A_GENRE]->(g:Genre)
        RETURN g.name AS genre, COUNT(m) AS nombre_films
        ORDER BY nombre_films DESC
        LIMIT 1
    """,
    "19. Films avec acteurs ayant joué avec vous": """
        MATCH (a:Actor)-[:A_JOUER]->(m:Film)<-[:A_JOUER]-(co_actor:Actor)
        RETURN DISTINCT m.title AS film
    """,
    "20. Réalisateur avec le plus d'acteurs distincts": """
        MATCH (d:Director)-[:DIRECTED]->(m:Film)<-[:A_JOUER]-(a:Actor)
        RETURN d.name AS realisateur, COUNT(DISTINCT a) AS nombre_acteurs
        ORDER BY nombre_acteurs DESC
        LIMIT 1
    """,
    "21. Films les plus connectés": """
        MATCH (m:Film)<-[:A_JOUER]-(a:Actor)-[:A_JOUER]->(other:Film)
        RETURN m.title AS film, COUNT(DISTINCT other) AS connexions
        ORDER BY connexions DESC
        LIMIT 5
    """,
    "22. 5 acteurs ayant joué avec le plus de réalisateurs": """
        MATCH (a:Actor)-[:A_JOUER]->(m:Film)<-[:DIRECTED]-(d:Director)
        RETURN a.name AS acteur, COUNT(DISTINCT d) AS nombre_realisateurs
        ORDER BY nombre_realisateurs DESC
        LIMIT 5
    """,
    "23. Recommandation de film selon genres d'un acteur": """
        MATCH (a:Actor {name: 'Leonardo DiCaprio'})-[:A_JOUER]->(m:Film)-[:A_GENRE]->(g:Genre)
        MATCH (rec:Film)-[:A_GENRE]->(g)
        WHERE NOT (a)-[:A_JOUER]->(rec)
        RETURN DISTINCT rec.title AS film_recommande
        LIMIT 5
    """,
    "24. Relation d'influence entre réalisateurs": """
        MATCH (d1:Director)-[:DIRECTED]->(m1:Film)-[:A_GENRE]->(g:Genre),
              (d2:Director)-[:DIRECTED]->(m2:Film)-[:A_GENRE]->(g)
        WHERE d1 <> d2
        MERGE (d1)-[:INFLUENCE_PAR]->(d2)
    """,
    "25. Plus court chemin entre Tom Hanks et Scarlett Johansson": """
        MATCH path = shortestPath(
            (a1:Actor {name: 'Tom Hanks'})-[:A_JOUER*]-(a2:Actor {name: 'Scarlett Johansson'})
        )
        RETURN path
    """,
    "26. Communautés d'acteurs (Louvain)": """
        CALL gds.graph.project(
            'actorGraph', ['Actor', 'Film'], {
                A_JOUER: {orientation: 'UNDIRECTED'}
            }
        )
        YIELD graphName
        CALL gds.louvain.stream('actorGraph')
        YIELD nodeId, communityId
        RETURN gds.util.asNode(nodeId).name AS acteur, communityId
        ORDER BY communityId
    """,
    "27. Films avec le plus de revenus et de votes": """
        MATCH (m:Film)
        WHERE m.revenue IS NOT NULL AND m.rating IS NOT NULL
        RETURN m.title AS film, m.revenue AS revenus, m.rating AS rating
        ORDER BY revenus DESC, rating DESC
        LIMIT 5
    """,
    "28. Acteurs ayant joué dans des films ayant le plus grand nombre de genres": """
        MATCH (a:Actor)-[:A_JOUER]->(m:Film)-[:A_GENRE]->(g:Genre)
        WITH a, m, COUNT(DISTINCT g) AS nombre_genres
        WHERE nombre_genres > 2
        RETURN a.name AS acteur, m.title AS film, nombre_genres
        ORDER BY nombre_genres DESC
        LIMIT 5
    """,
    "29. Acteur avec la plus longue carrière": """
        MATCH (a:Actor)-[:A_JOUER]->(m:Film)
        RETURN a.name AS acteur, MIN(m.release_year) AS debut, MAX(m.release_year) AS fin, (MAX(m.release_year) - MIN(m.release_year)) AS duree_carriere
        ORDER BY duree_carriere DESC
        LIMIT 1
    """,
    "30. Réalisateurs ayant travaillé sur le plus grand nombre de films différents": """
        MATCH (d:Director)-[:DIRECTED]->(m:Film)
        RETURN d.name AS realisateur, COUNT(DISTINCT m) AS nombre_films
        ORDER BY nombre_films DESC
        LIMIT 5
    """
}

if __name__ == "__main__":
    print("\nStarting Neo4j loading...\n")
    for question, query in questions_queries.items():
        print("=" * 60)
        print(f"Question: {question}")
        print("=" * 60)
        response = execute_query(query)
        print(response, "\n")
    print("All queries executed successfully!")