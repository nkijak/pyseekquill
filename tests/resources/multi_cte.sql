WITH cte_table as (select foo, bar from sub_table where foo = 1),
other_table as (select foo, bar from cte_table where bar > 'a')
SELECT bar
FROM other_table;
