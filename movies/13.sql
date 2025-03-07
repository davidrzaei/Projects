SELECT DISTINCT name FROM people
Where id IN
(SELECT person_id FROM stars
Where movie_id IN
(SELECT movie_id From stars
WHERE person_id IN
(SELECT id FROM people
WHERE name = 'Kevin Bacon'
AND birth = 1958)))
EXCEPT
SELECT name FROM people
WHERE people.name = "Kevin Bacon"
AND people.birth = 1958
ORDER BY name ASC;
