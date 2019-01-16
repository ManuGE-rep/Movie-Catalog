**MOVIE CATALOG**

**Description**

This application aims to show a catalog of movies. If you are not a user you
will be able to see some movies and it’s details. Instead, if you are logged as
a user via google, you will be able to add, update and delete your movies.

**Requirements**

To run this application you will need to have installed on your computer the
following softwares :

-   Virtualbox

-   Vagrant with a linux based virtual machine (ubuntu)

-   A pipenv virtual environment

You will also need to install python 3.7 or newer.

**Set up steps**

-   First, clone or download this project into a file of your choice.

-   Fire up your vagrant virtual machine with the two commands :

« vagrant up » and then « vagrant ssh ».

-   Move inside your folder with the cd command.

-   Install the requirements needed with the command :

« pipenv install -r requirements.txt ».

-   Run the database setup with « python dbsetup.py ».

-   Populate the database with « python fakedata.py ».

-   Run the application with the command :

« python application.py ».

-   Open the browser of your choice and type the following url :

<http://localhost:5000>.

That’s it ! You are now on the movie catalog.

**How it works**

You can browse different categories via the dropdown button on the top of the
page or simply click on an image to see the details of a movie.

To add a movie, click on the add new movie button.

To update a movie click on the edit button and finally to delete a movie, from
the movie details click on the delete button.

Remember, you must be logged in to access these options and you can only modify
or delete your own movies.
