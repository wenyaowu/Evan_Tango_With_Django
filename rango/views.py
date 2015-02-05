from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404 # Import the object 'HttpResponse'
from rango.models import Category, Page
from rango.form import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from bing_search import run_query


# What is view.py doing:
# view is a set of function which takes HttpRequest
# make corresponding HttpResponse.
# HttpResponse can include: 1) Original request
# 2) The template to render
# 3) some parameter that will be used in the render page (Send back as a dictionary object)

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]  # Sort by the likes in descending order
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "I'm BOLD", 'categories': category_list, 'pages':page_list}  # Dictionary connecting with template(html)

    if request.user.is_authenticated():
        context_dict['user'] = request.user

    visits = int(request.COOKIES.get('visits', '1'))
    if not visits:
        visits = 1
    reset_last_visit_time = False
    response = render(request, 'rango/index.html', context_dict)

# Does the cookie last_visit exist?
    if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value.
        last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).days > 0:
            visits = visits + 1
            # ...and flag that the cookie last visit needs to be updated
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True
        context_dict['visits'] = visits
        #Obtain our Response object early so we can add cookie information.
        response = render(request, 'rango/index.html', context_dict)
    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)
    # Return response back to the user, updating any cookies that need changed.
    return response


def about(request):
    context_dict = {'myname': "Evan"}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    result_list = []
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query']
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
    context_dict['result_list'] = result_list

    category = get_object_or_404(Category, slug=category_name_slug)
    if not context_dict['query']:
        context_dict['query']  = category.name
    context_dict['category'] = category
    context_dict['category_name']=category.name
    # Find all of the associated pages.
    # Note that filter returns >= 1 model instance.
    pages = Page.objects.filter(category=category).order_by('-views')
    context_dict['pages'] = pages # Contains several references
    context_dict['slug']= category_name_slug

    context_dict['request']=request
    return render(request, 'rango/category.html', context_dict)

@login_required
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

@login_required
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

@login_required
def restricted(request):
    return HttpResponse("Since you are logged in, you can see the text!")

def search(request):
    result_list=[]
    context_dict={}
    if request.method =='POST':
        query = request.POST['query']

        if query:
            result_list = run_query(query)
    context_dict['result_list']=result_list
    return render(request, 'rango/search.html', context_dict)


def track_url(request):
    url = '/rango/'
    page_id = None
    if request.method == 'GET':
        if 'page_id' in request.GET:
            print 'here'
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)
