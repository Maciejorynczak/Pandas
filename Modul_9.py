import pandas as pd

# Pobieranie danych
movies_data = pd.read_csv('C:/Users/macie/Downloads/tmdb_movies.csv')
genres_data = pd.read_csv(r'C:/Users/macie/Downloads/tmdb_genres.csv')

movies_data['release_date'] = pd.to_datetime(movies_data['release_date'], errors='coerce')
movies_data['release_year'] = movies_data['release_date'].dt.year

# Konwersja typu danych
movies_data['genre_id'] = movies_data['genre_id'].astype(str)
genres_data['genres'] = genres_data['genres'].astype(str)

# Zadanie 1: 
vote_count_threshold = movies_data['vote_count'].quantile(0.75)
top_rated_movies = movies_data[movies_data['vote_count'] > vote_count_threshold].nlargest(10, 'vote_average')

# Zadanie 2: 
grouped_data = movies_data[(movies_data['release_year'] >= 2010) & (movies_data['release_year'] <= 2016)]
grouped_data = grouped_data.groupby('release_year').agg({'revenue': 'mean', 'budget': 'mean'}).reset_index()

# Zadanie 3
merged_data = pd.merge(movies_data, genres_data, left_on='genre_id', right_on='genres', how='left')

# Zadanie 4
most_common_genre = merged_data['genres'].value_counts().idxmax()
most_common_genre_count = merged_data['genres'].value_counts().max()

print(f"Najczęściej występujący gatunek filmu: {most_common_genre}")
print(f"Liczba filmów w tym gatunku: {most_common_genre_count}")

#Zadanie 5
longest_runtime_genre = merged_data.groupby('genres')['runtime'].mean().idxmax()
longest_runtime = merged_data.groupby('genres')['runtime'].mean().max()

print(f"Gatunek filmu o najdłuższym średnim czasie trwania: {longest_runtime_genre}")
print(f"Średni czas trwania: {longest_runtime} minut")

# Zadanie 6
import matplotlib.pyplot as plt

# Filtrowanie danych dla gatunku o najdłuższym średnim czasie trwania
longest_runtime_genre_data = merged_data[merged_data['genres'] == longest_runtime_genre]

# Tworzenie histogramu czasu trwania filmów dla tego gatunku
plt.figure(figsize=(10, 6))
plt.hist(longest_runtime_genre_data['runtime'].dropna(), bins=20, color='blue', edgecolor='black')
plt.title(f'Histogram czasu trwania filmów dla gatunku: {longest_runtime_genre}')
plt.xlabel('Czas trwania (minuty)')
plt.ylabel('Liczba filmów')
plt.grid(True)
plt.show()
