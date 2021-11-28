# Distinctiveness and Complexity
- My web application is a website for a local gym. It is essentially an advertisement website for a gym, so it is not similar to any other projects from the course.
  - The website is also currently deployed at https://iron-arms-gym.herokuapp.com/. Website is hosted with Heroku, database is PostgreSQL, and static/media files are served using AWS-S3.
- This app utilizes Django, Bootstrap, JavaScript, Python (via Django), HTML, CSS, and SASS.
- The website utilizes JavaScript to display user reviews on the front-end by fetching them from the database and turning them into a slideshow with Bootstrap carousel.
- Django (and Python by association) is used to render every page and is also responsible for the search function in the equipment page, displaying equipment, and serializing user reviews into JSON from the database.
- There are two Django models, "Review" and "Equipment". 
  - The equipment model consists of an image, name, and description. Image is stored under a mediafiles directory. Equipment uploaded from the Django admin page are displayed in the equipment page.
  - The review model consists of a username, description, and star rating. Reviews uploaded from the Django admin page are displayed in the index page.
- The website is fully responsive, utilizing Bootstrap sizing classes across multiple viewports to make it appear aesthetic on every screen size.

## styles.scss, styles.css
Contains styling for every page in the website. Uses Bootstrap and SASS.

## bottom-navbar.js
Script for bottom navigation bar that determines whether it should be displayed in the viewport.
Bottom navigation bar will only fade into view if bottom of page is visible.

## index.js
Script for homepage that applies an animation to each parent element.
Elements slowly fade into view one by one.

## reviews.js
Script to fetch reviews from the database and display them in a bootstrap carousel.
Reviews cycle automatically, but can be navigated with navigation arrows or slide selectors.

## contact.html
Contact page that displays contact info.

## index.html
Home page that animates gym info and displays reviews.

## equipment.html
Equipment page to query and display gym equipment.

## location.html
Location page that displays a google map embed and location information about the gym.

## layout.html
Contains top navbar, bottom navbar, and header for other pages to inherit from.

## requirements.txt
Contains Python modules required to run app.

# Running App
To run the app, run the following commands in a command prompt. Python 3+ is required.
1. pip install django
2. pip install pillow
3. python manage.py runserver
- OPTIONAL: Testing suite is also included in app, but requires selenium and webdriver-manager.
  - pip install selenium
  - pip install webdriver-manager
  - python manage.py test

# Additional Information
My website is also currently deployed at https://iron-arms-gym.herokuapp.com/. Website is hosted with Heroku, models are stored in a PostgreSQL server, and static/media files are served using AWS-S3. I am currently working with the gym owner on developing this website, so there's still progress to be made!
