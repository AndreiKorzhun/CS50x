SELECT title FROM movies
JOIN stars ON stars.person_id = people.id
JOIN people ON stars.movie_id = movies.id
JOIN ratings ON ratings.movie_id = movies.id
WHERE people.name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5;