from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 # Import the object 'HttpResponse'
# Import the Category model
from rango.models import Category, Page
from rango.form import CategoryForm, PageForm


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]  # Sort by the likes in descending order
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "I'm BOLD", 'categories': category_list, 'pages':page_list}  # Dictionary connecting with template(html)
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'myname': "Evan"}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    # Can we find a category name slug with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # So the .get() method returns one model instance or raises an exception.
    category = get_object_or_404(Category, slug=category_name_slug)
    # category = Category.objects.get(slug=category_name_slug)  # find match
    context_dict['category_name']=category.name

    # Find all of the associated pages.
    # Note that filter returns >= 1 model instance.
    pages = Page.objects.filter(category=category)

    context_dict['pages'] = pages # Contains several references
    context_dict['category'] = category
    context_dict['slug']= category_name_slug
    #except Category.DoesNotExist:
    # We get here if we didn't find the specified category.
    # Don't do anything - the template displays the "no category" message for us.
    #raise Http404("Category doesn't exist")

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    # HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details
        # If there are errors, redisplay the form with error messages.
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm() # Other then POST
        context_dict = {'form':form, 'category':cat}
        return render(request, 'rango/add_page.html', context_dict)