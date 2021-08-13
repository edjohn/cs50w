from django.forms.widgets import Textarea, TextInput
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
from markdown2 import Markdown

from . import util

class EditForm(forms.Form):
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control'}))

class PageForm(EditForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        markdowner = Markdown()
        content = markdowner.convert(content)
    return render(request, "wiki/entry.html", {
        "title": title.capitalize(),
        "content": content,
        "entry_exists": util.get_entry(title) != None
    })

def search(request):
    formatted_query = request.GET['q'].lower()
    entries = util.list_entries()
    results = []
    for item in entries:
        formatted_item = item.lower()
        if formatted_query == formatted_item:
            return entry(request, formatted_query)
        if formatted_query in formatted_item:
            results.append(item)
    return render(request, "encyclopedia/search.html", {
        "results": results
    })
        
def create(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title.lower()):
                return render(request, "encyclopedia/create.html", {
                    "entry_exists": True,
                    "form": form
                })
            else:
                description = form.cleaned_data["description"]
                util.save_entry(title, description)
                return HttpResponseRedirect(reverse('encyclopedia:wiki') + title)
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": PageForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            util.save_entry(title, description)
            return HttpResponseRedirect(reverse('encyclopedia:wiki') + title)
        else:
            return render(request, "wiki/edit.html", {
                "form": form,
                "title": title
            })
    else:
        form = EditForm()
        form.fields['description'].initial = util.get_entry(title)
        return render(request, 'wiki/edit.html', {
            "form": form,
            "title": title
            })

def random(request):
    entries = util.list_entries()
    entry_name = choice(entries)
    return HttpResponseRedirect(reverse('encyclopedia:wiki') + entry_name)
        



