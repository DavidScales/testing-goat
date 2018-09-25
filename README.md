# Obey the Testing Goat

This repo contains my code and notes from working through the excellent [Obey the Testing Goat book](https://www.obeythetestinggoat.com/) on Test-Driven Development with Python.

## Dependencies

Install [geckodriver](https://github.com/mozilla/geckodriver/releases), which is a proxy that allows us to control Firefox programmatically via Selenium. Confirm installation:

```
geckodriver --version
```

Create a Python virtual environment, which enables us to configure & install a specific Python version and modules for the project directory:

```
python3.6 -m venv virtualenv
```

The `-m` flag tells Python to run the `venv` module directly (rather than as an imported library), and `virtualenv` is the directory name for the virtual environment files.

Activate the virtual environment:

```
source virtualenv/bin/activate
# deactivate with "deactivate"
```

Install Django and Selenium in the virtual environment:

```
pip install "django<1.12" "selenium<4"
```

WHAT ARE THESE FOR

## Getting started / chapter 1

Looks like the philosophy here is to always start with a test, which makes sense... An we are following the wisdom of the Testing Goat

> The Testing Goat is the unofficial mascot of TDD in the Python testing community

General process
1. write a test for what i want to do
2. run it and confirm that if fails as expected (important because it provides some confidence that we wrote the test correctly)
3. *then* write application code to do the thing I want

and along the way being sure to take small modular steps, so things never get out of hand

Start at the very beginning, even before setting up the framework boilerplate configuration. start with a functional test to spin up a browser instance using selenium, and check that Django is installed and that the dev server runs:

aside: functional tests vs unit tests

  from selenium import webdriver

  browser = webdriver.Firefox()
  browser.get('http://localhost:8000')

  assert 'Django' in browser.title

We run the test and get the expected failure ("Unable to connect"), which means we can start writing application code.

Create a Django "project", which represents the top level collection of files for our application:

```
django-admin.py startproject superlists .
```

This creates the Django boilerplate files & directory structure, along with the manage.py file that we use to do django stuffs.

WHAT ARE THESE FILES? (MAYBE)

such as starting the django dev server

python manage.py runserver

which allows us to pass the first test.

finally Things to add to **.gitignore**:

```
db.sqlite3
geckodriver.log
virtualenv
__pycache__
*.pyc
```

WHAT ARE THESE

### chapter 2, more philosphy & unittest

> Tests that use Selenium let us drive a real web browser, so they really let us see how the application functions from the user’s point of view. That’s why they’re called functional tests.

> This means that an FT can be a sort of specification for your application. It tends to track what you might call a User Story, and follows how the user might work with a particular feature and how the app should respond to them.

aka Acceptance tests, end-to-end tests, black box test

philosophy here:
1. start by using comments to create a "User Story" for a Minimum Viable Product (MVP) - the simplest app that is useful.
2. create functional tests to basically follow the user story. so for example

  from selenium import webdriver

  browser = webdriver.Firefox()

  # Edith has heard about a cool new online to-do app. She goes
  # to check out its homepage
  browser.get('http://localhost:8000')

  # She notices the page title and header mention to-do lists
  assert 'To-Do' in browser.title

  ...

comments are user story, code uses selenium to simulate a user.

--

Aside on comments - comments should *typically* be used to describe why some code does something, particularly when its not obvious. for example:

//

or the classic:

// dont change this because everything breaks and we dont know why

but in in general your code itself should describe *what* is happening. this should happen with variable and function names, code structure, etc. Because reading code is really important and writing readable code is almost never worse performing, so you might as well write it well. Additionally comments are annoying to maintain, because they need to always be updated with the code and will eventually become out of sync. Its subjective, but sometimes it makes more sense even to write code that is less concise if its more readable, IMO. for example

//

--

#### Python Standard Library's unittest Module

theres of course some common patterns that naturally evolve from testing, like logging details of failed tests, setting up and tearing down browser instances, etc. Python's unittest module has a lot of this built in

LATER I USE DJANGO's WHICH INHEREITS FORM UNITTEST
LiveServerTestCase

example

from selenium import webdriver
import unittest

  class NewVisitorTest(unittest.TestCase):

      def setUp(self):
          self.browser = webdriver.Firefox()

      def tearDown(self):
          self.browser.quit()

      def test_can_start_a_list_and_retrieve_it_later(self):
          # Edith has heard about a cool new online to-do app. She goes
          # to check out its homepage
          self.browser.get('http://localhost:8000')

          # She notices the page title and header mention to-do lists
          self.assertIn('To-Do', self.browser.title)
          self.fail('Finish the test!')

  if __name__ == '__main__':
      unittest.main(warnings='ignore')

* Tests are organize into classes inheriting fomr unittest.TestCase
* any method whose name starts with "test" will be run by the test runner, which is called with unittest.main()
* setUp and tearDown run before & after each test to ensure each test starts fresh (uneffected by other tests) and browser instances are cleaned up, etc.
* unittest provides helper methods like self.fail, self.assertIn, etc.

this logs a nicer formatted & more detailed report, handles cleanup, lets us use helpful methods, etc.

### chapter 3, django basics and unit tests


Django structures code into "apps", on the assumption that this will make them more modular and reusable. Apps are created with the manage.py startapp command, e.g.:

```
python manage.py startapp lists
```

which creates a folder for the app with basic boilerplate. One thing I found interesting is that app folders are on the same level with project folders (so lists & superlists are siblings), rather than apps living inside projects. Doesn't really matter, just though it was kind of weird since a project is theoretically made up of a collection of apps.

#### Unit tests

> functional tests test the application from the outside, from the point of view of the user. Unit tests test the application from the inside, from the point of view of the programmer.

philisohpy:
as you progress
1. write a functional test, describing the behavior from the users point of view (again, tracking the user story)
2. FT fails expectedly
3. write unit tests that describe how our solution code should behave
4. unit tests fail expectedly
5. write the smallest application code possible to pass the unit test
6. iterate - adding unit tests + application code cycles until the FT passes, and then adding more FT's and repeating.

--
double-loop.png
https://www.obeythetestinggoat.com/book/chapter_philosophy_and_refactoring.html
--

why - FT ensuring that stuff works as user expects and unit tests ensuring that out internals work as our programmers expect. small iterations ensure that as much of the application code as possible is "covered" by the tests (and that we dont sneak in a potential bug somehow by writing a complex method that we might not be testing thoroughly but passes the tests anyways)

> Functional tests should help you build an application with the right functionality, and guarantee you never accidentally break it. Unit tests should help you to write code that’s clean and bug free.

The django test file boilerplate

  from django.test import TestCase

  # Create your tests here.

imports an extended version of the standard library's unittest.TestCase with extra features.

Using the django test file allows us to use manage.py instead of running the test directly.

python manage.py test

which lets django do some extra fancy stuff for us

LIKE WHAT?

#### django basics

roughly MVC
* has models for sure
* views are more like controller
* templates are really the views

uses request response pairs like Express.

Django uses a file called urls.py to map URLs to view functions. There’s a main urls.py for the whole site in the the project folder (e.g., superlists/superlists)

So we could do something like this

  from django.conf.urls import url
  from lists import views

  urlpatterns = [
      url(r'^$', views.home_page, name='home'),
  ]

> A url entry starts with a regular expression that defines which URLs it applies to, and goes on to say where it should send those requests — ​either to a view function you’ve imported, or maybe to another urls.py file somewhere else

so in this case the empty string regex ^$ maps to a home_page view, which is just a function in the lists/views.py file. a simple example might be

  def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')

## Chapter 4 more of the same

philisoly
writing tests can be annoying for simple changes that seem trivial, but the idea is that, generally, complexity sneaks up over time, and you wont always be fresh or remember everything thats going on, and tests serve as a way to save your progress so to speak. the metaphor is pulling buckets of water from a well, its easy at first but eventually you get tired and the deeper the water is the hard the task becomes, and tests serve as a ratchet to ensure that you never slip backwards. writing tests for every single change is tedious, but its the only way to ensure that your not subjectively trying to guess when something is complex enough to warrant testing, which is a recipe for failure. additionally, if your writing tests for trivial changes, the tests themselves should be relatvialy trivial and thus not too bad to implement.

Selenium nuts and bolts

basically a browser driver, again kind of like simulating a user. has helpful methods like
find_element_by_id - find an element on the page
send_keys - type in input elements

more django

uses templates like other frameworks. example

<html>
    <title>To-Do lists</title>
</html>

these represent the views in MVC. so the previous example view function could be replaced with

from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')

where home.html is a template html file. django automatically looks for files in `templates` directories.

--
like other frameworks, its possible to pass variables into a template and have them render dynamic content. example:
--

One unintuitive thing with django is that you have to register your apps, by adding the app to the INSTALLED_APPS variable in the settings.py file. I'm not sure why creating the app initially with startapp doesnt automatically do this.

Django has a [test client](https://docs.djangoproject.com/en/1.11/topics/testing/tools/#the-test-client) which acts like a dummy web browser, a little like selenium. but unlike selenium its better suited for things like establishing that the correct template is being used in the correct context, and less suited for inspecting rendered html or webpage behavior. so its good for some unit tests but the FTs should stick with selenium. example:

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


TDD is super nice for refactoring because you can ensure that nothing was broken during the changes.

> When refactoring, work on either the code or the tests, but not both at once.

This is definitely a mistake ive made in the past where I start out refactoring something, and then along the way I just group in some small changes I wanted to make, and then something somewhere else breaks so i just fix that real quick, but that breaks somethign else, and then i have multiple changes and at least one bug and its all mixed in with the refactor. best to do it slowly peice by peice.

### Chapter 5 databases & object relational mapping



## Command cheat sheet

...

Dev server can be started with:

```
python manage.py runserver
```

Run tests with the following:

```
python manage.py test functional_tests/ # FT
python manage.py test friendsvoteapp/ # unit tests
python manage.py test # all
```

### Migrations

```
# make, view, and apply migrations
python manage.py makemigrations
ls friendsvoteapp/migrations
python manage.py migrate

# remove and create fresh DB
rm db.sqlite3
python manage.py migrate --noinput
```


### One off chores

```
# upgrade selenium
pip install --upgrade selenium

# check gecko driver version
geckodriver --version
```
