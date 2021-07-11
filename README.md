# change_password
The project implements the ChangePassword method as a ReSTful API. This also contains the automated unit tests for the defined functionalities. Uses the unittest mick library to mock the old password verification while testing the ChangePassword method.

The implemented password requiremnts are as follows:  
1. At least 18 alphanumeric characters and list of special chars !@#$&*  
2. At least 1 Upper case, 1 lower case ,least 1 numeric, 1 special character  
3. No duplicate repeat characters more than 4  
4. No more than 4 special characters  
5. 50 % of password should not be a number  

Test coverage is measured using the coverage module.
The API service is dockerized. 

## Installation
### Non-docker installation
1. You can use either the default `pip` or `pipenv` to install the dependencies; **requirements.txt** and **Pipfile.lock** are both furished for the sake.  
Installation through `pip`:
    ```
    pip install -r requirements.txt
    ```
    Installation through `pipenv`, requires you to install `pipenv` first:
    ```
    pipenv install
    ```

## Usage
### ChangePassword functionality
To check the functionality of the API, start the webserver
```
python webserver.py
```
Navigating to http://localhost:5000/ should show you the home page. The swagger documentation is hosted under http://localhost:5000/api/ui/ where you can manually test out the API.  
