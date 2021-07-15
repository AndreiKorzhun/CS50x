SELECT title FROM movies
JOIN stars ON stars.person_id = people.id
JOIN people ON stars.movie_id = movies.id
WHERE movies.id IN
(SELECT movies.id FROM movies
JOIN stars ON stars.person_id = people.id
JOIN people ON stars.movie_id = movies.id
WHERE people.name = 'Helena Bonham Carter')
AND  people.name = 'Johnny Depp';
