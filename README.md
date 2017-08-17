# django-react-template
Template for any Django-React based project with minimal setup required.

This setup is based on the tutorial found at <a href=https://hackernoon.com/creating-websites-using-react-and-django-rest-framework-b14c066087c7>this link.</a>

Make sure to install all of the project's dependencies:
<br>
<code>pip install -r requirements.txt</code>
<br>
<code>cd frontend</code>
<br>
<code>npm install</code>

In development, at least at the moment, the frontend runs from localhost:3000 and the backend runs from localhost:8000. To start the frontend, do the following:
<br>
<code>cd frontend</code>
<br>
<code>npm start</code>

And to start the backend run:
<br>
<code>cd backend</code>
<br>
<code>python manage.py runserver</code>

This uses Django-CORS-Headers module to allow cross-origin requests in development, however most will probably serve both from the same origin in production.
