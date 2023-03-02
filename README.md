# URL Shortener
This project provides a Python Flask based URL shortening service. The user can enter a long URL and receive a shorter, more manageable shortcode. Users can also provide their own shortcode. All shortcodes are of exactly 6 characters, and can be alphanumeric with underscores. 

The url shortner service saves the original URL and shortcode mappings in an Sqllite database. It also saves a count and timestamps of when a shortcode was created and last accessed. This data can be accessed using the service endpoints. 

# Prerequisites

To run the code, you will need Python 3+ and Python package installer pip. 

# Installation
1. Unzip the folder and navigate to it.
2. Open a terminal and install virtualenv using pip:

 ```
 pip install virtualenv
 ```
   
3. Create and activate a virtual environment:
 ```
 python -m venv shorturl
 source shorturl/bin/activate
 ```
   
 4. Install packages from requirements.txt:
 ```
 pip install -r requirements.txt
 ```
 
 5. Initialize the database:

```
python init_db.py
```

# Usage
To run the application, in the terminal at the root folder level, run the following command:
```
python app.py
```

# Testing
To run the tests, use the following command:
```
pytest url_shortener.py
```

**Note:** Run step #5 from installation steps before Testing to ensure that you start testing with a clean database loaded with some test data. 
