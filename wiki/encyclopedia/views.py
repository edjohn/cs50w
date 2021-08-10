from django.shortcuts import render
from django import forms

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "wiki/entry.html", {
        "title": title.capitalize(),
        "content": util.get_entry(title),
        "entry_exists": util.get_entry(title) != None
    })

def search(request):
    query = request.GET['q'].lower()
    entries = (map(lambda x: x.lower(), util.list_entries()))
    results = []
    for item in entries:
        if query == item:
            return entry(request, query)
        if query in item:
            results.append(item)
    return render(request, "encyclopedia/search.html", {
        "results": (map(lambda x: x.capitalize(), results))
    })
        

        



