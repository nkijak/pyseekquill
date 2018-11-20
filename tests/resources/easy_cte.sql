WITH cte_table as (select foo, bar from sub_table where foo = 1)
SELECT bar
FROM cte_table;
