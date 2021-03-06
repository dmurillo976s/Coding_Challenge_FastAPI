# Coding_Challenge_FastAPI

Implementation of coding challenge consisting of a simple REST API using the FastAPI framework.

Folder "api" contains the proper code implementations of the service. This includes the proper endpoint definitions and database interactions. SQLite was chosen as database engine, nevertheless the code was implemented as to flexibly allow for different database implementations.

Pytest was used as testing framework. Unit tests were implemented for endpoint interactions, using a mock database. Basic integration tests were also implemented for interactions with SQLite, this employing a "Temp" database.

Appropiate code comments are found in each module. In addition to this, in the folder "docs" is included an html file that corresponds to a static version of the OpenAPI documentation generated by accessing to the "/docs" endpoint of the FastAPI service ("http://localhost:8000/docs" for this example). This static version of the docs was generated for easier access, thanks to the code found in https://github.com/Redocly/redoc/issues/726.

Specific instructions were given as follows:


Coding challenge 

Requirement: 

Develop a basic Users/Teams CRUD REST API using the FASTAPI framework. The API should have the necessary methods to maintain and relate both entities. We use Google Spanner, but you are allowed to use the database of your preference. Please do not use an ORM.

Bonus Points: 

- [X] Include unit testing

- [ ] Deploy it on docker 

- [X] Use async methods 

- [X] Proper documentation

- [X] Use a relational database

Deliverable: 

Please send us a Github repository. 
