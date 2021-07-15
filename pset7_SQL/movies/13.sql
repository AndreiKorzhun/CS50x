SELECT DISTINCT(name) FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.id IN
(SELECT movies.id FROM movies
JOIN stars ON stars.person_id = people.id
JOIN people ON stars.movie_id = movies.id
WHERE people.name = 'Kevin Bacon'
AND birth = 1958)
AND name NOT IN
(SELECT name FROM people
WHERE name = 'Kevin Bacon' AND birth = 1958)

