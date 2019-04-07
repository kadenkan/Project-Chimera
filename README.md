# Project-Chimera
My final year project project, a novel hybrid user authentication scheme with multiple bases.

The codes here are for the webpage demo as a primitive implementation and display of Chimera.

- By Kan Ka Ho 54403181
- Project Code: 18CS110

## How to use the codes
First, you have to set up the environment for Django, a web framework. Below are the links for downloading it and doing so.

### Prequisites
Downloads:
- Python 3.7.3: https://www.python.org/downloads/
- PostgreSQL 10: https://www.postgresql.org/download/

Setting up Django:
1. Run `mkvirtualenv Project-Chimera` in the commandline terminal **(make sure you are in the Project-Chimera directory)**.
2. Run `pip install -r requirements.txt`, dependancies should be installed. 
3. Run `python manage.py migrate`. Tables of Chimera should be created in your PostgeSQL database.

### Running the web
Simply run `python manage.py runserver`, then click on the link provided or enter the link http://127.0.0.1:8000/ in your browser. It's done!

### Operatioins
You can register and login on the web page and gain the experience of using Chimera user authentication. Enjoy!

