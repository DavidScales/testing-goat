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

```
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
```

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

Django has a [test client](https://docs.djangoproject.com/en/1.11/topics/testing/tools/#the-test-client) which acts like a dummy web browser, a little like selenium. but unlike selenium its better suited for things like establishing that the correct template is being used in the correct context, and less suited for inspecting rendered html or webpage behavior. so its good for some unit tests but the FTs should stick with selenium. example unit test:

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


TDD is super nice for refactoring because you can ensure that nothing was broken during the changes.

> When refactoring, work on either the code or the tests, but not both at once.

This is definitely a mistake ive made in the past where I start out refactoring something, and then along the way I just group in some small changes I wanted to make, and then something somewhere else breaks so i just fix that real quick, but that breaks somethign else, and then i have multiple changes and at least one bug and its all mixed in with the refactor. best to do it slowly peice by peice.

### Chapter 5 databases & object relational mapping

aside
Some options on debugging unexpected functional test failures
* time.sleep can be used to pause text execution, and you can visually inspect the state of the browser
* classic print statements or manually visiting the site
* error messages in test assertions are nice because they offer a persistent improvement in debugging, unlike the above

aside
Handling CSRF tokens is pretty convenient in Django. All thats required is a "template tag":

    <form method="POST">
        <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
        {% csrf_token %}
    </form>

And the framework automatically inserts the appropriate token in a `<input type="hidden">`, and handles subsequent validation. And the dev server even catches forms without CSRF tokens during development! Pretty nice.

similarly, django allows dynamic rendering with template syntax like you would expect:

    <body>
        <h1>Your To-Do list</h1>
        <form method="POST">
            <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
            {% csrf_token %}
        </form>

        <table id="id_list_table">
            <tr><td>{{ new_item_text }}</td></tr>
        </table>
    </body>

    def home_page(request):
    return render(request, 'home.html', {
        'new_item_text': request.POST['item_text'],
    })

or

    <table id="id_list_table">
        {% for item in items %}
            <tr><td>1: {{ item.text }}</td></tr>
        {% endfor %}
    </table>

Python 3.6 f-strings
`f"New to-do item did not appear in table. Contents were:\n{table.text}"`

#### triangulation

to really ensure that tests are robust, they should be hard to "cheat". For example, if a test failed as follows:

    self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
    AssertionError: '1: Buy peacock feathers' not found in ['Buy peacock feathers']

I could cheat and change the application code to

    <tr><td>1: {{ new_item_text }}</td></tr>

which adds the missint "1:". Obviously this would be stupid, but the idea is that if I *could* cheat to pass a test, then maybe the test isn't that robust. Removing magic constants and hard-coded content will most likely solve the issue, but a more robust approach would be "triangulation". This just means that I write an additional test that prevents cheating. In this example something like:

    self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
    self.assertIn(
        '2: Use peacock feathers to make a fly',
        [row.text for row in rows]
    )

prevent cheating because the hard-coded application code would produce:

    <tr><td>1: Buy peacock feathers</td></tr>
    <tr><td>1: Use peacock feathers to make a fly</td></tr>

### Django ORM and Models

An Object-Relational Mapper is a layer of abstraction for data stored in a database - classes map tables, attributes map columns, and class instances map rows. Basically ORM’s let you use your high level language features (like classes) to interact with data instead of actually interfacing with the database yourself.

Django has a handy built in ORM.

So for example if I wanted to create a table of "Items" with a "text" column, I'd start by defining a simple Python class in models.py instead of writing any SQL or whatnot:

    from django.db import models

    class Item(models.Model):
        text = models.TextField(default='')

the Item class inherits from Django's Model class, and I can specify the columns I want with class attributes. In this case a "text" column, using the TextField() method to specify the type of the column (text), and the default arg to specify its default value. The models module also supports other column types like IntegerField, CharField, DateField, etc.

And now I have an ORM that models my database. but it doesnt actually build the database.

A migration system (is that the right wording?) is what's used to actually build and modify a database. Migrations allow adding/removing database tables and columns, and track the changes like a version control system.

In django a database can be built or modified with the `makemigrations` command:

    python manage.py makemigrations

which looks at models.py file that I just wrote and generates a migrations file, like `lists/migrations/0001_initial.py`

which has some python code that looks like it's used to create or modify a database from the corresponding model

    ...
    from django.db import migrations, models

    class Migration(migrations.Migration):
        initial = True
        dependencies = []
        operations = [
            migrations.CreateModel(
                name='Item',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ],
            ),
        ]

settings.py specifies the type of database (of which im sure django supports many). In this case its SQLite, which I've used before and just stores data in a file called db.sqlite3.
```
[...]
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

So to recap:
the migrations file (lists/migrations/0001_initial.py) was generated from my python models (models.py) using the `makemigrations` command. And the project settings (settings.py) specify the type of database that i want.

So now I can use the migrate command to actually create the database:

    python manage.py migrate

Then once you have models and a database, you can interact with the databse via teh models layer. So in tests and views:

You use regular python with the Models class API instead of SQL:

    from lists.models import Item

    class ItemModelTest(TestCase):

        def test_saving_and_retrieving_items(self):
            first_item = Item()
            first_item.text = 'The first (ever) list item'
            first_item.save()

            second_item = Item()
            second_item.text = 'Item the second'
            second_item.save()

            saved_items = Item.objects.all()
            self.assertEqual(saved_items.count(), 2)

            first_saved_item = saved_items[0]
            second_saved_item = saved_items[1]
            self.assertEqual(first_saved_item.text, 'The first (ever) list item')
            self.assertEqual(second_saved_item.text, 'Item the second')

Here I can instantiate a instance of the item model with Item(), and set the text attribute directly with first_item.text = 'The ...'.

The Model class's save() method lets use write the Item class instance to the DB (presumably as a row), and similarly we can use Model.objects.all() to query from the database, returning a list-like object that can be processed further with python.

For testing

Django's TestCase creates a separate test database from migrations (including unapplied ones, pre `migrate` command). so when you run your tests, a new clean DB is created, and then destroyed when the tests are finished. And actually I imagine the db is cleared in between the tests, so each is independent.

Aside
>Good unit testing practice says that each test should only test one thing. The reason is that it makes it easier to track down bugs. Having multiple assertions in a test means that, if the test fails on an early assertion, you don’t know what the status of the later assertions is.

The author makes a note about unit tests and databases:
> Purists will tell you that a "real" unit test should never touch the database, and that the test I’ve just written should be more properly called an integrated test, because it doesn’t only test our code, but also relies on an external system—​that is, a database.

So i should come back to this once I know more. TODO.

### upgrading FT's

In my case when working through building the app, my functional tests didnt actually use TestCase, instead relying only on Selenium. So no test database was create, and each time I ran an FT it was actually polluting my databse with a bunch of duplicate test entries. Which is firstly annoying, but also means that my functional tests are not independent.

This can be solved with `LiveServerTestCase`
* Like Django's Unittest, starts up a dev server and a uses a separate test DB, runs any method that starts with "test"

To use it, I have to move the functional test into a python module (just a directory with a __init__.py file), because thats what the django test runner expects.

so instead of functional_test.py its

    functional_test
    |-- __init__.py
    |-- test.py

Then instead of running the FT directly with like python functional_test.py, I use django's manage.py

    python manage.py test functional_test

and the new test.py file simply updates my original test from a simple python script like:

    from selenium import webdriver

    browser = webdriver.Firefox()

    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get('http://localhost:8000')

    # She notices the page title and header mention to-do lists
    assert 'To-Do' in browser.title

To something that looks more like my unit tests:

    from django.test import LiveServerTestCase
    ...

    class NewVisitorTest(LiveServerTestCase):

        def setUp(self):
            ...

Where functional tests are grouped with classes, and these classes inherit from LiveServerTestCase, which gives me the test dev server & database, and also setUp and tearDown methods to run in between tests.

The test dev server as its own url - live_server_url

###### Implicit and Explicit Waits

there are implicit & explicit waits
* implicit ones are when you leave it up to selenium to wait for some element or async operation. these are unreliable, and considered a bad idea even by the selenium team.
* explicit waits are where we tell selenium to wait a fixed time before looking for an element or do a thing. the issue here is that you dont want to wait too long (slow tests) and you dont want to wait too little (might get false negatives if something is just abnormally slow for some reason), and you really never know how long is long enough.

A good technique is to create a retry loop with a timeout:

from selenium.common.exceptions import WebDriverException

    MAX_WAIT = 10
    ...

        def wait_for_row_in_list_table(self, row_text):
            start_time = time.time()
            while True:
                try:
                    table = self.browser.find_element_by_id('id_list_table')
                    rows = table.find_elements_by_tag_name('tr')
                    self.assertIn(row_text, [row.text for row in rows])
                    return
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)

here we `try` to find an element in the DOM immediately, and if we can't, we pause for a small amount of time (500ms), and try again, up to some large amount of time (10seconds). This allows use to pass successful tests quickly, while ensuring that we wait long enough so as to not pass with a false position. I suppose a potential downside could be that we have to wait a long time for true negatives (when the test actaully shouwl fail), but those situations should happend much less often than the others. especially if youre running lots of tests, and you expect most of your tests to pass most of the time (at least in my experience so far).

> There are two types of exceptions we want to catch: WebDriverException for when the page hasn’t loaded and Selenium can’t find the table element on the page, and AssertionError for when the table is there, but it’s perhaps a table from before the page reloads, so it doesn’t have our row in yet.

In the example app this refactor shaved a couple seconds off the test time

### 7

Philosophy
* minimize upfront design because it takes time, and the end product almost always significantly deviates away from the design. It's more direct to have a minimal design, and iterate as problems arise or features become truly important.
* This spills over into the idea of YAGNI (You ain't gonna need it), which is the reality that most often, a lot of features and code simple end up unused and onyl serve to add complexity to the application. Better to start with the minimum set of functionality, as expand only as needed, to ensure that there is never excess.
* Representational State Transfer (REST) is a design approach for web API's, and can be useful inspiration (even if we don't follow it rigidly). For example

> REST suggests that we have a URL structure that matches our data structure, in this case lists and list items.

So each list can have its own URL

    /lists/<list identifier>/

new lists could be created with `/lists/new` and new items with `/lists/<list identifier>/add_item` (not exactly REST, which would probably use PUT or POST for these, but approximate)

is a good way to structure our site's API.


#### foreign key relationships

    from django.db import models

    class List(models.Model):
        pass

    class Item(models.Model):
        text = models.TextField(default='')
        list = models.ForeignKey(List, default=None)


#### capturing parameters from URLs

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/(.+)/$', views.view_list, name='view_list'),
]

(.+) is a capture group. captured text gets passed to view_list as an arg

def view_list(request, list_id):
    [...]

But this regex is greedy! it will also respond for /lists/1/more_stuff_here/


#### app urls vs project urls

before I had all the urls in urls.py file of the project (superlists/urls.py). But a better pattern is to move the app urls (url's for "list") into a urls.py file in the app itself (list/urls.py), and then to "include" the app urls into the project.

So that would look more like this:

superlists/urls.py (project)

    from django.conf.urls import include, url
    from lists import views as list_views
    from lists import urls as list_urls

    urlpatterns = [
        url(r'^$', list_views.home_page, name='home'),
        url(r'^lists/', include(list_urls)),
    ]

At the project level, i listen for a single url for the list app, which in this case is all URL's prefixed with `lists/`. The app url's are then `include`d. In other words, at the project level, we just listen for url's that start with `list/`, and then pass along those url's to the app level.

In the app, we just check the remainder of the url (after `list/`), and respond like were originally:

list/urls.py (app)

    from django.conf.urls import url
    from lists import views

    urlpatterns = [
        url(r'^new$', views.new_list, name='new_list'),
        url(r'^(\d+)/$', views.view_list, name='view_list'),
        url(r'^(\d+)/add_item$', views.add_item, name='add_item'),
    ]

In this configuration there is less duplication, and the url handling is more modular. the project level is just looking for which app to hand a request to, and the app itself handles the request.



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
