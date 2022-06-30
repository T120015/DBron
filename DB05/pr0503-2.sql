SELECT bo_books.title, bo_books.publish, bo_books.publish_date, bo_author.author_id, bo_author.name
FROM bo_authorbooks
INNER JOIN bo_author
ON bo_authorbooks.author_id = bo_author.author_id
INNER JOIN bo_books
ON bo_authorbooks.isbn = bo_books.isbn
;