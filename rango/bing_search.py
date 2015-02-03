__author__ = 'evanwu'
import json
import urllib, urllib2

BING_API_KEY = 'C3DDv/KwvvI4BmQ4haQ26kCYi0tVJUFxwrYzwLClBo8'

def run_query(search_terms):

    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    # Specify how many result we want to be in a page
    # Offset: Where to start
    results_per_page = 10
    offset = 0

    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stored within variable query.
    query = "'{0}'".format(search_terms)  # query = 'search_terms'
    query = urllib.quote(query) # Replace special characters in query using %xx escape

    # Construct the latter part of our request's URL.
    # Sets the format of the response to JSON and sets other properties.
    # The complete search url =
    # https://api.datamarket.azure.com/Bing/Search/v1/Web?$format=json&$top=10&$skip=0&Query='search_terms'
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url, #{0}
        source, #{1}
        results_per_page, #{2}
        offset, #{3}
        query #{4}
    )


    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''


    # Create a 'password manager' which handles authentication for us.
    # HTTPPasswordMgr.add_password(realm, uri, user, password)
    # This causes (user, passwd) to be used as authentication tokens
    # when authentication for realm and a super-URI of any of the given URIs is given.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)


    # Create empty results list
    results = []

    try:
        # Prepare for connecting to Bing's server
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        #Connect to the server and read the reponse
        response = urllib2.urlopen(search_url).read()

        # Convert String format response to a json dictionary object
        json_response = json.loads(response)

        # Loop through each page returned, put into our result list
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']
            })
    # Catch a URLError exception
    except urllib2.URLError, e:
        print "Something went wrong.", e

    return results
