import csv
from .data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        users = []
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({
                    'id': int(row['id']),
                    'name': row['name'],
                    'movies': []
                })
        return users

    def get_user_movies(self, user_id):
        movies = []
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['id']) == user_id:
                    movies.append({
                        'id': int(row['movie_id']),
                        'name': row['movie_name'],
                        'director': row['director'],
                        'year': int(row['year']),
                        'rating': float(row['rating'])
                    })
        return movies

    def add_user(self, name):
        users = self.get_all_users()
        user_id = max(user['id'] for user in users) + 1 if users else 1

        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, name])
        return user_id

    def add_movie(self, user_id, name, director, year, rating):
        movies = self.get_user_movies(user_id)
        movie_id = max(movie['id'] for movie in movies) + 1 if movies else 1

        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, movie_id, name, director, year, rating])
        return movie_id

    def update_movie(self, user_id, movie_id, name=None, director=None, year=None, rating=None):
        updated = False
        rows = []

        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[0]) == user_id and int(row[1]) == movie_id:
                    if name:
                        row[2] = name
                    if director:
                        row[3] = director
                    if year:
                        row[4] = year
                    if rating:
                        row[5] = rating
                    updated = True
                rows.append(row)

        if updated:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        return updated

    def remove_movie(self, user_id, movie_id):
        removed = False
        rows = []

        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[0]) == user_id and int(row[1]) == movie_id:
                    removed = True
                else:
                    rows.append(row)

        if removed:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        return removed
