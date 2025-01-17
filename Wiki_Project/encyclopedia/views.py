import random
import markdown2

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Route for the default wiki page
def wiki(request):
    return HttpResponse("WIKI")

# Route when a user accesses an entry through url
def title(request, title):

    entry_data = util.get_entry(title)
    # Checking if the entry exists
    if entry_data:
        entry_data_mark = markdown2.markdown(entry_data)
        return render(request, "encyclopedia/title.html", {
            "title": title.capitalize(),
            "entry_data": entry_data_mark
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title.capitalize(),
            "entry_data": None
        })
    

def search(request):

    # If user submitted his own data
    if request.method == "POST":
        
        # Getting data from html
        form_data = request.POST.get("q").strip().lower()

        # Now getting the entries from the function
        entries_data = util.list_entries()

        # Now checking if data exists in form
        for entry in entries_data:
            if entry.lower() == form_data:
                return redirect("title", title=entry)
            
        # Now the case if data doesnt exist
        matching_entries = [ entry for entry in entries_data if form_data in entry.lower() ]

        return render(request, "encyclopedia/search_results.html", {
            "query": form_data,
            "results": matching_entries
        })
    
    # If user got here through GET
    else:
        return render(request, "encyclopedia/index.html")
    
# If user wanna create a new page
def newpage(request):

    # If user submitted his data 
    if request.method == "POST":
        
        # Getting data from the form
        wiki_title = request.POST.get("wiki-title").strip()
        wiki_content = request.POST.get("wiki-content")

        # Now saving the entry to my list of entries
        checker = util.save_entry(wiki_title, wiki_content)

        # If entry saved successfully
        if checker:
            return redirect("title", title=wiki_title)
        
        else:
            return HttpResponse("Wikipedia page already exists")

    # If user got here through GET
    else:
        return render(request, "encyclopedia/newpage.html")
    

# If user clicks on the random button
def random_page(request):
    
    # First getting all the entries from the function
    all_entries = util.list_entries()

    if all_entries:
        random_entry = random.choice(all_entries)
        return redirect("title", title=random_entry)

    else:
        return HttpResponse("No entries found")
    

# If user wanna edit wiki page
def edit(request, title):

    # If user used POST to get here
    if request.method == "POST":

        # Getting the data from the form
        wiki_content = request.POST.get("wiki-content")

        # Saving the entry
        util.save_entry(title, wiki_content)

        # Redirecting to the sites page
        return redirect("title", title=title)
    
        # If user used GET to get here
    else:

        # First getting the entry data
        entry_data = util.get_entry(title)  
        
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry_data": entry_data
        })
    