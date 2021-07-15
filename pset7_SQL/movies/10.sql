SELECT DISTINCT(name) FROM people
JOIN directors ON directors.person_id = people.id
JOIN (SELECT id, title FROM movies
JOIN ratings ON ratings.movie_id = movies.id
WHERE rating >= 9.0) as video ON directors.movie_id = video.id;
