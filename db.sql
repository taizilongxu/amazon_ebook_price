CREATE TABLE books (
    book_id varchar(80) PRIMARY KEY,
    name varchar(300),
    author varchar(80),
    public_date varchar(80),
    create_date timestamp default current_timestamp
);

CREATE TABLE info (
    id integer PRIMARY KEY,
    book_id varchar(80),
    price numeric,
    comment_num integer,
    star numeric,
    create_date timestamp default current_timestamp
)