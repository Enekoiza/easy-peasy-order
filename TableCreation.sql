CREATE DATABASE EASYPEASY
    DEFAULT CHARACTER SET = 'utf8mb4';

CREATE TABLE EASYPEASY.PRODUCT(  
    product_name VARCHAR(255) COMMENT 'Product name',
    related_words VARCHAR(255) COMMENT 'Words related to the product',
    cost FLOAT(5) COMMENT 'Product cost',
    live int COMMENT 'item visibility',
    measure VARCHAR(100) COMMENT 'measure of the product',
    imageURL VARCHAR(200) COMMENT 'image that holds the product',
    product_id int AUTO_INCREMENT PRIMARY KEY
);


CREATE TABLE EASYPEASY.LANGUAGE(
    country VARCHAR(100) PRIMARY KEY COMMENT 'Country name',
    code VARCHAR(100) COMMENT 'Code needed for translation',
    live int COMMENT 'Implemented in the page',
    imageURL VARCHAR(255) COMMENT 'Country flag URL'
);

CREATE TABLE EASYPEASY.ADMINLOGIN(
    username VARCHAR(100) COMMENT 'username',
    password VARCHAR(100) COMMENT 'password'
);

CREATE TABLE EASYPEASY.ORDERS(
    OrderNo int PRIMARY KEY
);

CREATE TABLE EASYPEASY.ORDERS_PRODUCTS(
    product_id int,
    OrderNo int,
    quantity int,
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id),
    FOREIGN KEY (OrderNo) REFERENCES ORDERS(OrderNo),
    PRIMARY KEY (product_id, OrderNo)
);