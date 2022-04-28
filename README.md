# Easy-Peasy Order

This project uses SQL as database language, and Python 3.10 as the back end server language.

### Structural Query Language (SQL)

First you will need to have a SQL database.

If you don't have any SQL accessible you can download it from here:

- [Download SQL Database](https://dev.mysql.com/downloads/installer/)

Once the SQL Database server is downloaded, you must create the admin credentials which will be the creadentials to use to connect to the Database.

You must change the config.py file where all the database variables are stored.

### Python

This projects uses the last version of Python which is v3.10 and can be found in the next link:

- [Python downloads](https://www.python.org/downloads/)

## Google Speech to text Credentials

To make the voice recognition work you will need to add your own credentials by creating an account in google cloud.

For marking, the markers will have access to the file that must be placed in the main directory of the application.



## Deployment

These deployment instructions are exclusivelly for Windows 10.

Once the project is downloaded, go to the folder.

Now, you will need to install the libraries, they are all inside the Requirements.txt.

To install all of them, you should create a virtual enviroment.

To download the library that holds the virtual environment:

```bash
    pip install virtualenv
```

Create a new environment:
```bash
    virtualenv [environment name]
```

Activate the environment:

```bash
    [environment name]\Scripts\activate
```

Finally, install the libraries that will help run the project:

```bash
    pip install -r Requirements.txt
```

One more library will be needed (This library is to record the user's voice):

```bash
    pip install pipwin
    pipwin install pyaudio
```

Once the libraries are installed, you will need to set the environmental variables for Flask:

```bash
  set FLASK_ENV=development
  set FLASK_APP=app.py
```

Before running the project, you must **modify the config.py** to add the values of your SQL database

Run the project:

```bash
python app.py
```

If you have more than one version of python installed:

```bash
python3 app.py
```
