from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import requests

app = Flask(__name__)
data_manager = JSONDataManager('database.json')
omdb_api_key = "f465fdc9&t"


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            user_id = data_manager.add_user(name)
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            return "Name is required"
    else:
        return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.get_user_by_id(user_id)

    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']

        # Fetch additional movie details from OMDb API
        omdb_url = f'http://www.omdbapi.com/?apikey={omdb_api_key}={title}'
        response = requests.get(omdb_url)
        if response.status_code == 200:
            movie_data = response.json()
            director = movie_data['Director']
            year = movie_data['Year']
            rating = movie_data['imdbRating']

        if name and director and year and rating:
            movie_id = data_manager.add_movie(user_id, name, director, year, rating)
            if movie_id:
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return "Failed to add movie. Try again!"
        else:
            return "All fields are required"
    else:
        return render_template('add_movie.html', user=user)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return "User not found"

    movie = data_manager.get_movie_by_id(user_id, movie_id)
    if not movie:
        return "Movie not found"

    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        if name and director and year and rating:
            if data_manager.update_movie(user_id, movie_id, name, director, year, rating):
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return "Failed to update movie. Try again!"
        else:
            return "All fields are required"
    else:
        return render_template('update_movie.html', user=user, movie=movie)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    user = data_manager.get_user_by_id(user_id)
    if data_manager.remove_movie(user_id, movie_id):
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return "Failed to delete movie. Try again!"


if __name__ == "__main__":
    app.run(debug=True)
