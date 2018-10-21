# Obey the Testing Goat

This repo contains my code and (rough) notes from working through the excellent [Obey the Testing Goat book](https://www.obeythetestinggoat.com/) on Test-Driven Development with Python.

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

[Django](https://www.djangoproject.com/) is a Python web framework. [Selenium](https://www.seleniumhq.org/) is many things, but practically speaking, it's a library for driving web browsers.

## Chapter 1 - getting started

### Philosophy and first test

Looks like the basic Test Driven Development (TDD) philosophy is to always start with a test, which makes sense...

General process
1. write a test for what I want to do
2. run it and confirm that if fails as expected (this is important because it provides some confidence that we wrote the test correctly)
3. *then* write application code to do the thing I want

and along the way being sure to take small modular steps, so things never get out of hand.

Start at the very beginning, even before setting up the framework boilerplate configuration. Start with a functional test to spin up a browser instance using selenium, and check that Django is installed and that the dev server runs. For example:

    # functional_test.py

    from selenium import webdriver

    browser = webdriver.Firefox()
    browser.get('http://localhost:8000')

    assert 'Django' in browser.title

We run the test (`python functional_test.py`) and get the expected failure "Unable to connect", which means we can start writing application code.

Selenium also has a ton of useful methods like:
* `find_element_by_id` - find an element on the page
* `send_keys` - type in input elements
* etc.

### Configuring Django boilerplate

Create a Django "project", which represents the top level collection of files for our application:

    django-admin.py startproject superlists .

This creates the Django boilerplate files & directory structure, along with the manage.py file that we use to do Django stuff. For example, starting Django's dev server:

    python manage.py runserver

Which allows the first test to pass.

The following Django + selenium files can be git ignored (added to `.gitignore`):
* `db.sqlite3` - the file that represents the default sqlite database
* `geckodriver.log` - probably a log for selenium driver errors
* `virtualenv` - the Python virtual environment config files
* `__pycache__` - probably some kind of Python runtime cache
* `*.pyc`- probably some kind of Python runtime cache
* `/static` - from Ch8, copies of static files for serving in production


## Chapter 2 - more philosophy & Python's unittest

### Functional tests and user stories

What are "functional" (FT) tests?

> Tests that use Selenium let us drive a real web browser, so they really let us see how the application functions from the user’s point of view. That’s why they’re called functional tests.

> This means that an FT can be a sort of specification for your application. It tends to track what you might call a User Story, and follows how the user might work with a particular feature and how the app should respond to them.

FT's are AKA Acceptance tests, end-to-end tests, and black box tests.

Expanding the TDD philosophy:
1. start development by using comments to create a "User Story" for a Minimum Viable Product (MVP) - the simplest app that is useful.
2. create functional tests to basically follow the user story. So for example:

```
from selenium import webdriver

browser = webdriver.Firefox()

# Edith has heard about a cool new online to-do app. She goes
# to check out its homepage
browser.get('http://localhost:8000')

# She notices the page title and header mention to-do lists
assert 'To-Do' in browser.title

...
```

Comments make up the user story, and selenium is used to simulate a user.

### A comment on comments

Comments should typically be used to describe *why* some code does something, rather than what the code does, particularly when the code's purpose is not obvious. For example:

    ## We use a new browser session to make sure that no information
    ## of Edith's is coming from cookies, etc.
    self.browser.quit()

Where it's not obvious why you're quitting the browser instance. Or the classic:

    # dont change this because everything breaks and we dont know why

But in in general your code itself should describe *what* is happening. This should be communicated with variable and function names, code structure, etc. Because reading code is really important and writing readable code is almost never worse performing, so you might as well write it well.

Additionally comments are annoying to maintain, because they need to always be updated with the code and will eventually become out of sync. It's subjective, but sometimes it makes more sense even to write code that is less concise if it's more readable, in my opinion. For example:

    // Not sure what name really means or how I got it?
    const name = retrieve('/data/users?q=income').people.filter(person => person.age > 100)[0].name;

    // Ah I see
    const usersByIncome = retrieve('/data/users?q=income');
    const centenarianByIncome = usersByIncome.people.filter(person => person.age > 100);
    const highestIncomeCentenarian = centenarianByIncome[0];
    const highestIncomeCentenarianName = highestIncomeCentenarian.name;

### Python Standard Library's unittest Module

There's of course some common patterns that naturally evolve from testing, like logging details of failed tests, setting up and tearing down browser instances, etc. Python's `unittest` module has a lot of this functionality built in. For example, in the following:

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

* Tests are organize into classes inheriting from `unittest.TestCase`
* Any method whose name starts with "test" will be run by the test runner, which is called with `unittest.main()`
* `setUp` and `tearDown` run before & after each test to ensure each test starts fresh (unaffected by other tests) and browser instances are cleaned up, etc.
* `unittest` provides helper methods like `self.fail`, `self.assertIn`, etc.

Note: Django has it's own test runner and class, which inherits from `unittest`. See chapter 5 & 6 notes.

## Chapter 3 - Django basics and unit tests

### Django basics

Django structures code into "apps", on the assumption that this will make them more modular and reusable. Apps are created with the `manage.py` `startapp` command, e.g.:

    python manage.py startapp lists

which creates a folder for the app with basic boilerplate.

One thing I found interesting is that app folders are on the same level with project folders (so `lists` & `superlists` are siblings), rather than apps living inside projects. Doesn't really matter, just though it was kind of odd since a project is theoretically made up of a collection of apps, and I would expect the app folders to be children in the project folder.

### Unit tests

> functional tests test the application from the outside, from the point of view of the user. Unit tests test the application from the inside, from the point of view of the programmer.

Extending the TDD philosophy again. The new process is:
1. write a functional test, describing the behavior from the users point of view (again, tracking the user story)
2. FT fails expectedly
3. write unit tests that describe how our solution code should behave
4. unit tests fail expectedly
5. write the smallest application code possible to pass the unit test
6. iterate - adding unit tests + application code cycles until the FT passes, and then adding more FT's and repeating.

![TDD process flowchart](double-loop.png)
https://www.obeythetestinggoat.com/book/chapter_philosophy_and_refactoring.html

Why do I need these extra tests?
* FTs ensure that stuff works as user expects and unit tests ensure that internals work as programmers expect.
* Small iterations ensure that as much of the application code as possible is "covered" by the tests (and that we dont sneak in a potential bug somehow by writing a complex method that we might not be testing thoroughly but passes the tests anyways).

> Functional tests should help you build an application with the right functionality, and guarantee you never accidentally break it. Unit tests should help you to write code that’s clean and bug free.

### Django unit test boilerplate

Django has a boilerplate test file:

    from django.test import TestCase

    # Create your tests here.

which imports an extended version of the Python standard library's `unittest.TestCase` with extra features. The tests here can be run with Django's test runner via manage.py:

    python manage.py test

Using Django's test runner enables additional functionality like spinning up test databases.

### Django basics

* Django roughly follows the common MVC pattern
  * has models for sure
  * views are more like the controller
  * templates are really the views
* Django uses request-response pairs like Express.
* Django uses a file called `urls.py` to map URLs to view functions.

There’s a main `urls.py` for the whole site in the the project folder (e.g., `superlists/urls.py`)

So we could do something like this:

    # superlists/urls.py

    from django.conf.urls import url
    from lists import views

    urlpatterns = [
        url(r'^$', views.home_page, name='home'),
    ]

Where

> A url entry starts with a regular expression that defines which URLs it applies to, and goes on to say where it should send those requests — ​either to a view function you’ve imported, or maybe to another urls.py file somewhere else

So in this case the empty string regex `^$` maps to a `home_page` view, which is just a function in the `lists/views.py` file. A simple example might be:

    # lists/views.py

    def home_page(request):
      return HttpResponse('<html><title>To-Do lists</title></html>')

## Chapter 4 - a little more of everything

### A TDD metaphor

* Writing tests can be annoying for simple changes that seem trivial, but the idea is that, generally, complexity sneaks up over time, and you wont always be fresh or remember everything thats going on, and tests serve as a way to sort of save your progress.

* The metaphor is pulling buckets of water from a well - it's easy at first but eventually you get tired and the deeper the water is, the harder the task becomes. Tests serve as a ratchet to ensure that you never slip backwards.

* Writing tests for every single change is tedious, but it's the only way to ensure that your not subjectively trying to guess when something is complex enough to warrant testing, which is a recipe for failure. Additionally, if you're writing tests for trivial changes, the tests themselves should be relatively trivial and thus not too bad to implement.

### More Django basics

#### Templates

Django uses templates like other frameworks. For example:

    # templates/home.html

    <html>
        <title>To-Do lists</title>
    </html>

These represent the views in the MVC pattern. So the previous example view function:

    # lists/views.py

    def home_page(request):
      return HttpResponse('<html><title>To-Do lists</title></html>')

could be replaced with:

    # lists/views.py

    from django.shortcuts import render

    def home_page(request):
        return render(request, 'home.html')

Where `home.html` is a template HTML file. Django automatically looks for files in `templates` directories.

And of course, like other frameworks, it's possible to pass variables into a template and have them render dynamic content. For example:

    <table id="id_list_table">
        <tr><td>{{ new_item_text }}</td></tr>
    </table>

#### Registering apps

One unintuitive gotcha (at least for me) with Django is that you have to register your apps, by adding the app to the `INSTALLED_APPS` variable in the `settings.py` file. I'm not sure why creating the app initially with `startapp` doesn't automatically do this.

#### Test client

Django has a [test client](https://docs.djangoproject.com/en/1.11/topics/testing/tools/#the-test-client) which acts like a dummy web browser, a little like selenium. But unlike selenium it's better suited for things like establishing that the correct template is being used in the correct context, and less suited for inspecting rendered HTML or webpage behavior. So it's good for some unit tests but the FTs should stick with selenium. Example unit test:

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

Here the testing `client` gets a url, and asserts that the correct template was used.

#### TDD and refactoring

TDD is super nice for refactoring because you can ensure that nothing was broken during the changes.

> When refactoring, work on either the code or the tests, but not both at once.

This is definitely a mistake I've made myself in the past, where I start out refactoring something, and then along the way I just group in some small changes I wanted to make, and then something somewhere else breaks so I just fix that real quick, but that breaks something else, and then I have multiple changes and at least one bug and it's all mixed in with the refactor. Best to do it slowly piece by piece.

## Chapter 5 - more fundamentals, databases, & object relational mapping

### CSRF and dynamic templating

Handling CSRF tokens is pretty convenient in Django. All thats required is a "template tag":

    <form method="POST">
        <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
        {% csrf_token %}
    </form>

And the framework automatically inserts the appropriate token in a `<input type="hidden">`, and handles subsequent validation. And the dev server even catches forms without CSRF tokens during development! Pretty nice.

Similarly, Django allows dynamic rendering with template syntax like you would expect:

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
            <tr><td>{{ item.text }}</td></tr>
        {% endfor %}
    </table>

### Triangulation

To really ensure that tests are robust, they should be hard to "cheat". For example, if a test failed as follows:

    self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
    AssertionError: '1: Buy peacock feathers' not found in ['Buy peacock feathers']

I could cheat and change the application code to:

    <tr><td>1: {{ new_item_text }}</td></tr>

Which adds the missing `1:`. Obviously this would be stupid, but the idea is that if I *could* cheat to pass a test, then maybe the test isn't that robust. Removing magic constants and hard-coded content will most likely solve the issue, but a more robust approach would be "triangulation". This just means that I write an additional test that prevents cheating. In this example something like:

    self.assertIn(
      '1: Buy peacock feathers',
      [row.text for row in rows])
    self.assertIn(
      '2: Use peacock feathers to make a fly',
      [row.text for row in rows]
    )

prevents cheating because the hard-coded application code would produce:

    <tr><td>1: Buy peacock feathers</td></tr>
    <tr><td>1: Use peacock feathers to make a fly</td></tr>

### Django ORM and Models

An Object-Relational Mapper is a layer of abstraction for data stored in a database, e.g.:
* classes map tables
* attributes map columns
* class instances map rows

Basically ORM’s let you use your high level language features (like classes) to interact with data instead of actually interfacing with the database yourself.

Django has a handy built in ORM.

So for example if I wanted to create a table of "Items" with a "text" column, I'd start by defining a simple Python class in `models.py` instead of writing SQL or whatnot:

    from django.db import models

    class Item(models.Model):
        text = models.TextField(default='')

The `Item` class inherits from Django's `Model` class, and I can specify the columns I want with class attributes. In this case a "text" column, using the `TextField()` method to specify the type of the column (text), and the default argument to specify its default value. The models module also supports other column types like `IntegerField`, `CharField`, `DateField`, etc.

And now I have an ORM that models my database. But it doesn't actually build the database.

A migration system is what's used to actually build and modify a database. Migrations allow adding/removing database tables and columns, and track the changes like a version control system.

In Django a database can be built or modified with the `makemigrations` command:

    python manage.py makemigrations

which looks at the `models.py` file that I just wrote and generates a migrations file, like `lists/migrations/0001_initial.py`.

This migrations file has some Python code that looks like it's used to create or modify a database from the corresponding model:

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

The `settings.py` specifies the type of database (of which I'm sure Django supports many). In this case it's SQLite, which I've used before and just stores data in a file called `db.sqlite3`. Example `settings.py` database config:

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

* So to recap - the migrations file (`lists/migrations/0001_initial.py`) was generated from my Python models (`models.py`) using the `makemigrations` command. And the project settings (`settings.py`) specify the type of database that I want to use.

So now I can use the `migrate` command to actually create (or modify) the database:

    python manage.py migrate

Then once you have models and a database, you can interact with the database via the models layer. So in tests and views, you use regular Python with the Models class API instead of SQL:

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

Here I can instantiate an instance of the item model with `Item()`, and set the `text` attribute directly with `first_item.text = 'The ...'`.

The Model class's `save()` method lets us write the `Item` class instance to the DB (presumably as a row), and similarly we can use `Model.objects.all()` to query from the database, returning a list-like object that can be processed further with Python.

Django's `TestCase` also creates a separate test database from migrations (including unapplied ones, that haven't yet been applied with the `migrate` command. I assume this is so you can test your migrations before applying them). So when you run your tests, a new clean DB is created, and then destroyed when the tests are finished. And actually I imagine the DB is cleared in between the tests, so each is independent.

An author's note:

>Good unit testing practice says that each test should only test one thing. The reason is that it makes it easier to track down bugs. Having multiple assertions in a test means that, if the test fails on an early assertion, you don’t know what the status of the later assertions is.

The author also makes a note about unit tests and databases:

> Purists will tell you that a "real" unit test should never touch the database, and that the test I’ve just written should be more properly called an integrated test, because it doesn’t only test our code, but also relies on an external system—​that is, a database.

So I should come back to this once I know more. TODO:.

### Upgrading FT's

In my case when working through building the app, my functional tests didn't actually use TestCase, instead relying only on Selenium. So no test database was created, and each time I ran an FT it was actually polluting my database with a bunch of duplicate test entries. Which is firstly annoying, but also means that my functional tests are not independent.

This can be solved with `LiveServerTestCase`, which like Django's `unittest.TestCase`, starts up a dev server and a uses a separate test DB, running any method that starts with "test".

To use it, I have to move the functional test into a Python module (which is apparently just a directory with an `__init__.py` file), because that's what the Django test runner expects.

So instead of `functional_test.py` at the project root, it's

    functional_test
    |-- __init__.py
    |-- test.py

Then instead of running the FT directly with like `python functional_test.py`, I use Django's `manage.py` command:

    python manage.py test functional_test

And the new `test.py` file simply updates my original tests from a simple Python script like:

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

Where functional tests are grouped with classes, and these classes inherit from `LiveServerTestCase`, which gives me the test dev server & database, and also `setUp` and `tearDown` methods to run in between tests.

The test dev server as its own URL - `live_server_url`.

### Implicit and Explicit Waits

There are implicit & explicit waits
* implicit ones are when you leave it up to selenium to wait for some element or async operation. These are often unreliable, and considered a bad idea even by the selenium team.
* explicit waits are where we tell selenium to wait a fixed amount of time before looking for an element or doing a thing. The issue here is that you dont want to wait too long (because your tests will be unnecessarily slow) and you dont want to wait too little (because you might get false negatives if something is just abnormally slow for some reason), and you really never know how long is long enough.

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

Here we `try` to find an element in the DOM immediately, and if we can't, we pause for a small amount of time (500ms), and try again, up to some large amount of time (10 seconds).

> There are two types of exceptions we want to catch: WebDriverException for when the page hasn’t loaded and Selenium can’t find the table element on the page, and AssertionError for when the table is there, but it’s perhaps a table from before the page reloads, so it doesn’t have our row in yet.

This allows use to pass successful tests quickly, while ensuring that we wait long enough so as to not fail with a false negative. I suppose a potential downside could be that we have to wait a long time for true negatives (when the test actually should fail), but those situations should happen much less often than the others (especially if you're running lots of tests, and you expect most of your tests to pass most of the time, which is the case in my experience with testing so far).

In the example app, this refactor shaved a couple seconds off the test time.

## Chapter 7 - design notes and more Django features

More philosophy, this time extending past TDD into [agile](https://en.wikipedia.org/wiki/Agile_software_development) and general software design:

* minimize upfront design because it takes time, and the end product almost always significantly deviates away from the original design. It's more direct to have a minimal design, and iterate as problems arise or features become truly important.
* This spills over into the idea of YAGNI (You ain't gonna need it), which is the reality that most often, a lot of features and code simple end up unused and only serve to add complexity to the application. Better to start with the minimum set of functionality, as expand only as needed, to ensure that there is never excess.
* Representational State Transfer (REST) is a design approach for web API's, and can be useful inspiration (even if we don't follow it rigidly). For example:

> REST suggests that we have a URL structure that matches our data structure, in this case lists and list items.

So each list can have its own URL

    /lists/<list identifier>/

New lists could be created with `/lists/new` and new items with `/lists/<list identifier>/add_item` (not exactly REST, which would probably use PUT or POST for these, but approximate).

This is a good (and common) way to structure a web app's API.

### Foreign key relationships

Example for creating foreign key relationships in the Django ORM:

    from django.db import models

    class List(models.Model):
        pass

    class Item(models.Model):
        text = models.TextField(default='')
        list = models.ForeignKey(List, default=None)


### Capturing parameters from URLs

URL parameters can be captured similarly to regular expressions (at least how I've seen it done in JavaScript):

    urlpatterns = [
        url(r'^$', views.home_page, name='home'),
        url(r'^lists/new$', views.new_list, name='new_list'),
        url(r'^lists/(.+)/$', views.view_list, name='view_list'),
    ]

Where `(.+)` is a capture group. Captured text gets passed to the corresponding view function (e.g., `view_list`) as an argument:

    def view_list(request, list_id):
        [...]

But this regex is greedy! it will also respond for `/lists/1/more_stuff_here/`.

### App URLs vs Project URLs

Before, I had all the URLs in the project's `urls.py` file (`superlists/urls.py`). But a better pattern is to move the app URLs (URLs for "list") into a `urls.py` file in the app itself (`list/urls.py`), and then to "include" the app URLs into the project.

So that would look more like this:

    # superlists/urls.py (project)

    from django.conf.urls import include, url
    from lists import views as list_views
    from lists import urls as list_urls

    urlpatterns = [
        url(r'^$', list_views.home_page, name='home'),
        url(r'^lists/', include(list_urls)),
    ]

At the project level, I listen for a single url for the list app, which in this case is all URLs prefixed with `lists/`. The app URLs are then `include`d. In other words, at the project level, we just listen for URLs that start with `list/`, and then pass along those URLs to the app level.

In the app, we just check the remainder of the url (after `list/`), and respond like were originally:

    # list/urls.py (app)

    from django.conf.urls import url
    from lists import views

    urlpatterns = [
      url(r'^new$', views.new_list, name='new_list'),
      url(r'^(\d+)/$', views.view_list, name='view_list'),
      url(r'^(\d+)/add_item$', views.add_item, name='add_item'),
    ]

In this configuration there is less duplication, and the URL handling is more modular. The project level is just looking for which app to hand a request to, and the app itself handles the request.

## Chapter 8 - Testing layout, styling, and static files

### Testing aesthetics

* Testing aesthetics is pretty much like testing constants, so it doesn't make sense to test in detail
* What you really want is a "smoketest", to make sure that your site is being styled and, for example, nothing has gone wrong with the loading of static assets like CSS sheets
* You could also probably test important JavaScript heavy styling

Example smoketest - make sure CSS loads by checking approximate page style:

    class NewVisitorTest(LiveServerTestCase):
        ...

        def test_layout_and_styling(self):
            # Edith goes to the home page
            self.browser.get(self.live_server_url)
            self.browser.set_window_size(1024, 768)

            # She notices the input box is nicely centered
            inputbox = self.browser.find_element_by_id('id_new_item')
            self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=10
            )

Here we add a test case which sets the browser window size and checks that the main input is centered (which is what our styling does). `assertAlmostEqual` is used for rounding errors, scrollbars, etc.

### Template inheritance in Django

Just like I would expect - reduces redundancy and makes changes way easier since you don't have to update multiple pages that share the same basic structure.

Create a base template with "blocks" for other templates to inject content:

    <!-- lists/templates/base.html -->

    <html>
      <head>
        <title>To-Do lists</title>
      </head>

      <body>
        <h1>{% block header_text %}{% endblock %}</h1>
        <form method="POST" action="{% block form_action %}{% endblock %}">
          <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
          {% csrf_token %}
        </form>
        {% block table %}
        {% endblock %}
      </body>
    </html>

Then other templates can simple `extend` the base template by injecting their specific content into the blocks:

    <!-- lists/templates/home.html -->

    {% extends 'base.html' %}

    {% block header_text %}Start a new To-Do list{% endblock %}

    {% block form_action %}/lists/new{% endblock %}

### Static files in Django

> Django, and indeed any web server, needs to know two things to deal with static files:
1. How to tell when a URL request is for a static file, as opposed to for some HTML that’s going to be served via a view function
2. Where to find the static file the user wants

For #1, Django has a URL "prefix" to identify static files. The default is `/static/`, and is defined in `settings.py`:

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.11/howto/static-files/

    STATIC_URL = '/static/'

I had expected that this would be the end of static file configuration, since I've effectively mapped all URLs with `/static/` to files that I expect to server statically. However it's apparently a bit more complicated, and here's what I learned from the [docs](https://docs.djangoproject.com/en/1.7/howto/static-files/#staticfiles-testing-support):

* Django uses the `django.contrib.staticfiles` app to manage static files. This app is (or should be) registered in the `INSTALLED_APPS` variable of the `settings.py` file. Django (or maybe `django.contrib.staticfiles` specifically) looks in `setting.py`'s `STATIC_URL` for the name of the static files directory, which is `/static/` by default.
* You can then reference static files in the app as hard-coded values like `/static/my_app/myexample.jpg`, or ideally using the [static template tag](https://docs.djangoproject.com/en/1.7/howto/static-files/#staticfiles-testing-support) to build a URL dynamically. TODO: The book isn't cover the latter, so I'll come back to that later.
* In either case the static files are stored in `my_app/static/`, so for example `my_app/static/my_app/myexample.jpg`
  * This URL is interesting because it has a nested directory structure. This is because when looking for files, Django simply returns the first file with a matching name. So if another app had a similarly named file, like:

        app_one/static/myexample.jpg
        app_two/static/myexample.jpg

    You could get the wrong file. Thats why you need namespacing, like:

        app_one/static/app_one/myexample.jpg
        app_two/static/app_two/myexample.jpg

Anyways, apparently all this configuration so far doesn't actually serve any static files...

* It seems that in production, there is a `STATIC_ROOT` directory (set in `settings.py`) where Django can collect static files for serving. The `collectstatic` command is used to copy files from all the apps' `/static/` folders to the `STATIC_ROOT`. Then you can use a web server to serve the files from that directory.
  * Why?
  > using Python to serve raw files is slow and inefficient, and a web server like Apache or Nginx can do this all for you. You might even decide to upload all your static files to a CDN, instead of hosting them yourself. For these reasons, you want to be able to gather up all your static files from inside their various app folders, and copy them into a single location, ready for deployment.
  * example using relative paths: `STATIC_ROOT = os.path.join(BASE_DIR, 'static')`

* During development
  * the dev server (`runserver`) will search out the static files automatically when `DEBUG=True`.
  * However, unlike the dev server, `LiveServerTestCase` assumes static content has been collected under `STATIC_ROOT`, and does not use the `staticfiles` app to search for `/static/` directories.
    * So there is a separate app to get around this - `django.contrib.staticfiles.testing.StaticLiveServerTestCase`, which behaves like the dev server, and serves the static files without having to collect them under `STATIC_ROOT`.

* Aside: You can also have a static files directory outside of your apps for non-app-specific resources.

TODO:
* checkout SASS & LESS
* checkout the [static template tag](https://docs.djangoproject.com/en/1.7/howto/static-files/#staticfiles-testing-support)

## Command cheat sheet

Dev server can be started with:

    python manage.py runserver

Run tests with the following:

    python manage.py test functional_tests/ # FT
    python manage.py test friendsvoteapp/ # unit tests
    python manage.py test # all

### Migrations

    # make, view, and apply migrations
    python manage.py makemigrations
    ls friendsvoteapp/migrations
    python manage.py migrate

    # remove and create fresh DB
    rm db.sqlite3
    python manage.py migrate --noinput

### One off chores

    # upgrade selenium
    pip install --upgrade selenium

    # check gecko driver version
    geckodriver --version
