__author__ = 'evanwu'
# Setting the environment variable DJANGO_SETTINGS_MODULE to be the project setting file
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Evan_Tango_With_Django.settings')

import django
django.setup()  # Import the django settings

from rango.models import Category, Page  # Import Django models


def populate():
    python_cat = add_cat('Python')
    python_cat.views = 128
    python_cat.likes = 64
    python_cat.save()

    add_page(python_cat,
             title="Offcial Python tutorial",
             url="http://docs.python.org/2/tutorial/")

    add_page(python_cat,
             title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/")

    add_page(python_cat,
             title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat('Django')
    django_cat.views = 64
    django_cat.likes = 32
    django_cat.save()

    add_page(django_cat,
             title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(django_cat,
             title="Django Rocks",
             url="http://www.djangorocks.com/")

    add_page(django_cat,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/")

    other_cat = add_cat('Other Frameworks')
    other_cat.views = 32
    other_cat.likes = 16
    other_cat.save()

    add_page(other_cat,
             title="Bottle",
             url="http://bottlepy.org/docs/dev/")

    add_page(cat=other_cat,
             title="Flask",
             url="http://flask.pocoo.org")

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))  # Print out what've been added

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]  # Reference of the object created
    return c                                          # [0] means the first element in the return tuple


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

# Start execution
if __name__ == '__main__':
    print "Start populating..."
    populate()