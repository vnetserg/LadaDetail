DROP DATABASE IF EXISTS dbcourse;

CREATE DATABASE dbcourse
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

USE dbcourse;

CREATE TABLE customer(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstname varchar(50) NOT NULL,
    lastname varchar(50) NOT NULL,
    middlename varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    birthdate date NOT NULL,
    regdate date NOT NULL,
    passport varchar(250) NULL,
    phone varchar(20) NULL
);

CREATE TABLE shop(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(100) NULL,
    description varchar(100) NULL,
    address varchar(250) NULL,
    phone varchar(20) NULL
);

CREATE TABLE employee(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstname varchar(50) NOT NULL,
    lastname varchar(50) NOT NULL,
    middlename varchar(50) NOT NULL,
    birthdate date NOT NULL,
    passport varchar(250) NULL,
    address varchar(250) NULL,
    department varchar(100) NOT NULL,
    shop_id INT NOT NULL,
    position varchar(100) NOT NULL,
    empdate date NOT NULL,
    salary int NOT NULL,

    FOREIGN KEY (shop_id)
        REFERENCES shop(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE orders(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    employee_id INT NOT NULL,
    shop_id INT NOT NULL,
    regdate date NOT NULL,
    price INT NOT NULL DEFAULT 0,

    FOREIGN KEY (customer_id)
        REFERENCES customer(id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (employee_id)
        REFERENCES employee(id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (shop_id)
        REFERENCES shop(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE car(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(50) NOT NULL,
    description varchar(1000) NOT NULL,
    proddate date NOT NULL,
    photo varchar(100) NULL
);

CREATE TABLE detail(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    article varchar(50) NOT NULL,
    name varchar(50) NOT NULL,
    description varchar(1000) NOT NULL,
    photo varchar(100) NULL,
    category varchar(50) NOT NULL,
    warranty int NOT NULL,
    price int NOT NULL
);

CREATE TABLE order_detail(
    order_id INT NOT NULL,
    detail_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),

    PRIMARY KEY (order_id, detail_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (detail_id)
        REFERENCES detail(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE shop_detail(
    shop_id INT NOT NULL,
    detail_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),

    PRIMARY KEY (shop_id, detail_id),

    FOREIGN KEY (shop_id)
        REFERENCES shop(id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (detail_id)
        REFERENCES detail(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE car_detail(
    car_id INT NOT NULL,
    detail_id INT NOT NULL,

    PRIMARY KEY (car_id, detail_id),

    FOREIGN KEY (car_id)
        REFERENCES car(id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    FOREIGN KEY (detail_id)
        REFERENCES detail(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);