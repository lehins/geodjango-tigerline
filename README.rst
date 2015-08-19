This app is intended to make it easier to add TIGER/Line data to a GeoDjango project and save people from writing this same code over and over (collectively).

It is not (yet) exhaustive, it's just what I had and have needed in the past.
If you have models / load scripts for other data in the set, please fork/add and send me a pull request if you add other shapefiles. If you come up with useful manager methods, I'd love to see those too.

*NOTE: If you need cities, the best source for that is the US National Atlas. I have an app for those at https://github.com/adamfast/usgsdata-citiesx020

It's been tested and used with Django 1.1 to 1.4 and PostGIS + PostgreSQL. ORM freezing South
migrations are included as well, I'm currently using the 0.7.3 version.

Download data
-------------

Download shape files for one of the years 2012-2014. Tigerline files for states
(./STATES/), counties (./COUNTY/) and/or subcounties (./COUSUB/):

* http://www2.census.gov/geo/tiger/TIGER2012/
* http://www2.census.gov/geo/tiger/TIGER2013/
* http://www2.census.gov/geo/tiger/TIGER2014/

Unzip the files.

Configure
---------

* Configure ``django.contrib.gis`` as described in the `django docs <https://docs.djangoproject.com/en/>_`.
* Make sure ``'django.contrib.gis'`` and ``'tigerline'`` are in ``INSTALLED_APPS``.

* Customize the models you want to use.

.. code-block::python

    TIGERLINE_MODELS = (
      ('zipcode', None),
      ('nation', 'myapp.Nation'),
      ('division', 'myapp.Division'),
      ('state', 'myapp.State'),
      ('county', 'myapp.County'),
      ('subcounty', 'myapp.SubCounty')
    )




run `python manage.py syncdb` or `python manage.py migrate` as approporiate

If you want to import all three:
run `python manage.py load_tigerline --path=~/Path/to/shapefiles`

Or there are individual management commands if you only need one set:
run `python manage.py load_counties --path=~/Path/to/shapefiles`
run `python manage.py load_states --path=~/Path/to/shapefiles`
run `python manage.py load_zipcodes --path=~/Path/to/shapefiles`
