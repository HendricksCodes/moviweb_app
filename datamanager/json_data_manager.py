import json
from datamanager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
        return data

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=2)

    def get_all_users(self):
        return [user['name'] for user in self.data]

    def get_user_movies(self, user_id):
        for user in self.data:
            if user['id'] == user_id:
                return user.get('movies', [])
        return []

    def add_user(self, name):
        user_id = max(user['id'] for user in self.data) + 1 if self.data else 1
        user = {
            'id': user_id,
            'name': name,
            'movies': []
        }
        self.data.append(user)
        self.save_data()
        return user_id

    def add_movie(self, user_id, name, director, year, rating):
        user = self.get_user_by_id(user_id)
        if user:
            movie_id = max(movie['id'] for movie in user['movies']) + 1 if user['movies'] else 1
            movie = {
                'id': movie_id,
                'name': name,
                'director': director,
                'year': year,
                'rating': rating
            }
            user['movies'].append(movie)
            self.save_data()
            return movie_id
        return None

    def update_movie(self, user_id, movie_id, name=None, director=None, year=None, rating=None):
        movie = self.get_movie_by_id(user_id, movie_id)
        if movie:
            if name:
                movie['name'] = name
            if director:
                movie['director'] = director
            if year:
                movie['year'] = year
            if rating:
                movie['rating'] = rating
            self.save_data()
            return True
        return False

    def remove_movie(self, user_id, movie_id):
        user = self.get_user_by_id(user_id)
        if user:
            for movie in user['movies']:
                if movie['id'] == movie_id:
                    user['movies'].remove(movie)
                    self.save_data()
                    return True
        return False

    def get_user_by_id(self, user_id):
        for user in self.data:
            if user['id'] == user_id:
                return user
        return None

    def get_movie_by_id(self, user_id, movie_id):
        user = self.get_user_by_id(user_id)
        if user:
            for movie in user['movies']:
                if movie['id'] == movie_id:
                    return movie
        return None
