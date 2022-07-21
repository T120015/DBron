-- (1)
use sampledb;
select *
from uri_sales
inner join uri_shop
on uri_sales.s_id = uri_shop.s_id
;

-- (2)
select uri_shop.s_id, uri_shop.s_name , sum(uri_sales.s_value) as goukei
from uri_sales
inner join uri_shop
on uri_sales.s_id = uri_shop.s_id
group by uri_shop.s_id
;

-- (3)

select * 
from bo_books
inner join bo_category
on bo_books.category_id = bo_category.category_id
inner join bo_authorbooks
on bo_books.isbn = bo_authorbooks.isbn
;

-- (4)
select * 
from bo_books
inner join bo_category
on bo_books.category_id = bo_category.category_id
inner join bo_authorbooks
on bo_books.isbn = bo_authorbooks.isbn
inner join bo_author
on bo_author.author_id = bo_authorbooks.author_id 
;

