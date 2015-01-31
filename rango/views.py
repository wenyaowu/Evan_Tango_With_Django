from django.shortcuts import render
from django.http import HttpResponse # Import the object 'HttpResponse'
# Import the Category model
from rango.models import Category, Page


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]  # Sort by the likes in descending order

    context_dict = {'boldmessage': "I'm BOLD", 'categories': category_list}  # Dictionary connecting with template(html)
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'myname': "Evan"}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name']=category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages # Contains several references
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    return render(request, 'rango/category.html', context_dict)
