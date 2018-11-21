SELECT f.foo, s.bar
FROM first_table as f
INNER JOIN second_table as s
ON f.id = s.id;
