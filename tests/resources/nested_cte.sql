with outer_table as (
  with first_inner as (
    select b, d from real_table_1)
  select b, d from first_inner
)
select b, d from outer_table;
