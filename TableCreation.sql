CREATE DATABASE EASYPEASY
    DEFAULT CHARACTER SET = 'utf8mb4';

CREATE TABLE PRODUCT(  
    product_name VARCHAR(255) COMMENT 'Product name',
    related_words VARCHAR(255) COMMENT 'Words related to the product',
    cost FLOAT(5) COMMENT 'Product cost',
    live int(1) COMMENT 'item visibility',
    measure VARCHAR(100) COMMENT 'measure of the product',
    imageURL VARCHAR(200) COMMENT 'image that holds the product',
    product_id int(10) AUTO_INCREMENT PRIMARY KEY
) DEFAULT CHARSET UTF8 COMMENT '';


CREATE TABLE LANGUAGE(
    country VARCHAR(100) PRIMARY KEY COMMENT 'Country name',
    code VARCHAR(100) COMMENT 'Code needed for translation',
    live int(1) COMMENT 'Implemented in the page',
    imageURL VARCHAR(255) COMMENT 'Country flag URL'
) DEFAULT CHARSET UTF8 COMMENT '';

CREATE TABLE ADMINLOGIN(
    username VARCHAR(100) COMMENT 'username',
    password VARCHAR(100) COMMENT 'password'
)DEFAULT CHARSET UTF8 COMMENT '';

CREATE TABLE ORDERS(
    OrderNo int(10) PRIMARY KEY
)DEFAULT CHARSET UTF8 COMMENT '';

CREATE TABLE ORDERS_PRODUCTS(
    product_id int(10),
    OrderNo int(10),
    quantity int(10),
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id),
    FOREIGN KEY (OrderNo) REFERENCES ORDERS(OrderNo),
    PRIMARY KEY (product_id, OrderNo)
)