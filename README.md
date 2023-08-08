# Grocery Store
## create virtual enviroment
```
command: pip install virtualenv
```
```
command: virtualenv <venv_name>
```
- use requirements.txt to install compatible packages
```
command: pip install -r requirment.txt
```
- To run flask server
```
command: python app.py
```

## Description
Grocery store is an application same as e-commerce website to create a direct link between customers & the shop like Amazon, eBay or Walmart etc. It is an app which has 2 phases: one is for Admin & other one is for Users.<br><br>
Admin phase with features like creation, updation or deletion of any product/ category as per change due to customer requirements or due to any of circumstances like change in govt. policy etc..<br>
User phase with features like search, add-to-cart, remove-from-cart, order of any product etc..<br><br>
It consists of 2 APIs for CRUD operations on CATEGORY and PRODUCT
<br><br>
### Technologies used
1. Python (Programming Language)
2. Flask (Web Framework)
3. HTML (Web Page)
4. Bootstrap (Frontend)
5. Flask-SQLAlchemy==3.0.5 (SQLite connection)
6. Jinja2==3.1.2 (HTML injection)
7. SQLAlchemy==2.0.19 (SQLite connection)
8. Werkzeug==2.3.6 (To secure file)
9. Seaborn==0.12.2 (Data Visualization)

## APIs are for CRUD Operations on CATEGORY and PRODUCT
- For CATEGORY
```
GET:- localhost:8080/category_api/{id}
```
```
GET:- localhost:8080/category_api/
```
```
POST:- localhost:8080/category_api/
```
```
PUT:- localhost:8080/category_api/{id}
```
```
DELETE:- localhost:8080/category_api/{id}
```

- For PRODUCT
```
GET:- localhost:8080/product_api/{id}
```
```
GET:- localhost:8080/product_api/
```
```
POST:- localhost:8080/product_api/
```
```
PUT:- localhost:8080/product_api/{id}
```
```
DELETE:- localhost:8080/product_api/{id}
```
# Architecture and Features
└── MAD-1-Project<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── 22f2000957Report.pdf<br>
&nbsp;&nbsp;&nbsp;&nbsp;└── CODE<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── static<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── templates<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── admin.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── API.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── API.yaml<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── app.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── controller.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── database.sqlite3<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── model.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── requirements.txt<br>

### For testing purpose, use this email_id password:
email_id: shivani@gmail.com<br>
password: 12345
