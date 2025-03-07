SELECT name FROM people
WHERE id IN
(Select person_id from stars
where movie_id IN
(Select id from movies
Where title = 'Toy Story'));
