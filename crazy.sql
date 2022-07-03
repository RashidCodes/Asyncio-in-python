if object_id('dbo.test_table') is not null  
    drop table dbo.test_table;

create table dbo.test_table (
    ident int identity(1,1),
    name varchar(20)
);

insert into dbo.test_table values ('rashid'), ('mohammed'), ('dev'), ('nanie'), ('bernadette'), ('penny'), ('leonard'), ('raj'), ('stuart'), ('howard'), ('sheldon');
go 

with a as (
    select  
        t1.ident as t9ident,
        t1.name as t1name,
        t2.name as t2name,
        t3.name as t3name,
        t4.name as t4name,
        t5.name as t5name,
        t6.name as t6name,
        t7.name as t7name,
        t8.name as t8name,
        t9.name as t9name
    from dbo.test_table t1 
    cross apply dbo.test_table t2 
    cross apply dbo.test_table t3 
    cross apply dbo.test_table t4 
    cross apply dbo.test_table t5
    cross apply dbo.test_table t6 
    cross apply dbo.test_table t7 
    cross apply dbo.test_table t8 
    cross apply dbo.test_table t9 -- add more cross apply operators to expand 
    cross apply dbo.test_table t10
    where t1.ident > t2.ident
        and t2.ident > t3.ident 
        and t3.ident > t4.ident
        and t4.ident > t5.ident 
        and t5.ident > t6.ident 
        and t6.ident > t7.ident
        and t7.ident > t8.ident 
        and t8.ident > t9.ident
        and t9.ident > t10.ident
),

b as (
    select *,
     row_number() over (partition by t9ident order by t9ident) as row_num
    from a
)

select * 
from b 
where row_num < 2

