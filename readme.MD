# MyBlogs
## This is a simple example of blogging website.

### Technologies Used:
### FrontEnd:
### HTML
### CSS
### Javascript

### BackEnd:
### Flask - Python 3.10
### MySQL (MySQL command line client 5.5)

## Tables

|----------------|
| Tables_in_work |
|----------------|
| blogs          |
| users          |
|----------------|

## Table 1: users

| Field          | Type         | Null | Key | Default | Extra          |
|----------------|--------------|------|-----|---------|----------------|
| id             | int(11)      | NO   | PRI | NULL    | auto_increment |
| first_name     | varchar(20)  | NO   |     | NULL    |                |
| last_name      | varchar(20)  | YES  |     | NULL    |                |
| username       | varchar(30)  | NO   | UNI | NULL    |                |
| email          | varchar(50)  | NO   |     | NULL    |                |
| password       | varchar(200) | NO   |     | NULL    |                |
| image_location | varchar(100) | YES  |     | /       |                |
| total_posts    | int(11)      | NO   |     | 0       |                |


## Table 2: blogs

| Field     | Type          | Null | Key | Default           | Extra                       |
|-----------|---------------|------|-----|-------------------|-----------------------------|
| id        | int(11)       | NO   | PRI | NULL              | auto_increment              |
| poster    | varchar(30)   | NO   |     | NULL              |                             |
| title     | varchar(200)  | NO   |     | NULL              |                             |
| content   | varchar(2000) | NO   |     | NULL              |                             |
| date_time | timestamp     | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
