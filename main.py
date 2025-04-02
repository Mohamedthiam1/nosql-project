from database import get_movies
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Gettin' all movies to see
movies = get_movies()


# 1. Afficher l’année où le plus grand nombre de films ont été sortis.
years = [movie.get('year') for movie in movies if movie.get('year')] 
if years:
    year_counts = Counter(years)
    most_films_year = year_counts.most_common(1)[0]
    print(f"L'année avec le plus grand nombre de films: {most_films_year[0]} avec {most_films_year[1]} films.")
else:
    print("Aucune année valide trouvée.")

# 2. Quel est le nombre de films sortis après l'année 1999?
count_after_1999 = sum(1 for movie in movies if movie.get('year', 0) > 1999)
print(f"Nombre de films sortis après 1999: {count_after_1999}")

# 3. Quelle est la moyenne des votes des films sortis en 2007?
films_2007 = [movie for movie in movies if movie.get('year') == 2007]
average_rating_2007 = sum(float(movie['rating']) if movie['rating'].replace('.', '', 1).isdigit() 
                          else 0 for movie in films_2007) / len(films_2007) if films_2007 else 0
print(f"Moyenne des votes des films sortis en 2007: {average_rating_2007}")

# 4. Affichez un histogramme qui permet de visualiser le nombre de films par année.
plt.hist(years, bins=range(min(years), max(years) + 1), edgecolor='black')
plt.title('Nombre de films par année')
plt.xlabel('Année')
plt.ylabel('Nombre de films')
plt.show()

# 5. Quelles sont les genres de films disponibles dans la base?
genres = {genre for movie in movies for genre in movie.get('genre', '').split(',')}
print(f"Genres disponibles dans la base: {genres}")

# 6. Quel est le film qui a généré le plus de revenu?
highest_revenue_movie = max(movies, key=lambda x: x.get('Revenue (Millions)', 0) or 0)
print(f"Le film qui a généré le plus de revenu: {highest_revenue_movie['title']} avec {highest_revenue_movie['Revenue (Millions)']}")

# 7. Quels sont les réalisateurs ayant réalisé plus de 5 films dans la base de données?
directors = [movie.get('Director') for movie in movies if movie.get('Director')]
director_counts = Counter(directors)
directors_more_than_5 = [director for director, count in director_counts.items() if count > 5]
print(f"Réalisateurs ayant réalisé plus de 5 films: {directors_more_than_5}")

# 8. Quel est le genre de film qui rapporte en moyenne le plus de revenus?
genre_revenue = defaultdict(list)
for movie in movies:
    for genre in movie.get('genre', '').split(','):
        revenue = movie.get('Revenue (Millions)', None)
        if revenue and revenue != '': 
            genre_revenue[genre].append(revenue)

average_revenue_by_genre = {
    genre: sum(revenues) / len(revenues) if revenues else 0
    for genre, revenues in genre_revenue.items()
}

highest_avg_revenue_genre = max(average_revenue_by_genre, key=average_revenue_by_genre.get)
print(f"Le genre qui rapporte en moyenne le plus de revenus: {highest_avg_revenue_genre}")

# 9. Quels sont les 3 films les mieux notés (rating) pour chaque décennie (1990-1999, 2000-2009, etc.)?
decades = defaultdict(list)
for movie in movies:
    decade = (movie.get('year', 0) // 10) * 10  
    if movie.get('rating') != 'unrated':  
        decades[decade].append(movie)

top_movies_by_decade = {}
for decade, decade_movies in decades.items():
    top_movies = sorted(decade_movies, key=lambda x: x.get('rating', 0), reverse=True)[:3]
    top_movies_by_decade[decade] = top_movies

for decade, top_movies in top_movies_by_decade.items():
    print(f"Top 3 films de {decade}s:")
    for movie in top_movies:
        title = movie.get('title')
        rating = movie.get('rating')
        
        if title and rating: 
            print(f"  {title} - {rating}")

# 10. Quel est le film le plus long (Runtime) par genre?
genre_runtime = defaultdict(lambda: {'runtime': 0, 'movie': None})

for movie in movies:
    runtime = movie.get('Runtime (Minutes)', None)
    
    if runtime and isinstance(runtime, (int, float)):  
        for genre in movie.get('genre', '').split(','):
            if runtime > genre_runtime[genre]['runtime']:
                genre_runtime[genre] = {'runtime': runtime, 'movie': movie}

for genre, data in genre_runtime.items():
    if data['movie']:  
        print(f"Le film le plus long dans le genre {genre}: {data['movie']['title']} ({data['runtime']} min)")
    else:
        print(f"Pas de film trouvé pour le genre {genre}.")

# 12. Calculer la corrélation entre la durée des films (Runtime) et leur revenu
    runtime = [
    float(movie.get('Runtime (Minutes)', 0)) 
    for movie in movies 
    if isinstance(movie.get('Runtime (Minutes)', 0), (int, float)) and isinstance(movie.get('Revenue (Millions)', 0), (int, float))
]

revenue = [
    float(movie.get('Revenue (Millions)', 0)) 
    for movie in movies 
    if isinstance(movie.get('Runtime (Minutes)', 0), (int, float)) and isinstance(movie.get('Revenue (Millions)', 0), (int, float))
]

if len(runtime) > 1 and len(revenue) > 1:
    correlation = np.corrcoef(runtime, revenue)[0, 1]
else:
    correlation = 0

print(f"Corrélation entre la durée des films et leur revenu: {correlation}")

# 13. Y a-t-il une évolution de la durée moyenne des films par décennie?
decade_runtime = defaultdict(list)
for movie in movies:
    decade = (movie.get('year', 0) // 10) * 10 
    if 'Runtime (Minutes)' in movie:
        decade_runtime[decade].append(movie['Runtime (Minutes)'])

average_runtime_by_decade = {decade: sum(runtimes) / len(runtimes) for decade, runtimes in decade_runtime.items()}

for decade, avg_runtime in sorted(average_runtime_by_decade.items()):
    print(f"Durée moyenne des films dans les années {decade}s: {avg_runtime:.2f} minutes")