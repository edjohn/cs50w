from django.shortcuts import render

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
