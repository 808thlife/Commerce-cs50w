from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid, Comments

import datetime

class createListing(forms.ModelForm):
    title = forms.CharField(label= "Title", max_length = 32)
    description = forms.CharField(label= "Description", max_length = 499)
    price = forms.IntegerField(label = "Price", max_value = 10000000000)
    img = forms.ImageField(label = "Image")
    class Meta:
        model = Category
        exclude = ('categoryName',)

    def save(self, commit = True):
        listing = super(createListing, self).save(commit = False)
        listing.title = self.cleaned_data['title']
        listing.description = self.cleaned_data['description']
        listing.price = self.cleaned_data['price']
        listing.img = self.cleaned_data['img']

        if commit:
            listing.save()

        return listing
    
    categories = forms.ModelChoiceField(queryset = Category.objects.all(), empty_label= "Select a Category" )

class bidForm(forms.Form):
    new_bid = forms.IntegerField(label = "Your offer")

class CategoriesForm(forms.Form):
    sel_category = forms.ModelChoiceField(queryset = Category.objects.all(), empty_label= "Select a Category" )

class CommentsForm(forms.Form):
    comment = forms.CharField(max_length=300)

def index(request):
    content = Listing.objects.all()
    message = ''
    if not request.user.is_authenticated:
        message = "Please, log in to see the page"
    context = {"listings":content, 'message':message}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def categoriesPage(request):
        CategoriesList = Category.objects.all()
        context = {'list':CategoriesList}
        return render(request, "auctions/categories.html", context)

def watchCat(request,catID, catTitle):
    list_cats = Listing.objects.filter(categories_id = catID)
    context = {'listings':list_cats}
    return render(request, f'auctions/watchCategory.html', context)

def addcomment(request,itemID):
    currentUser = request.user
    listingData = Listing.objects.get(id = itemID)
    if request.method == "POST":
        message = request.POST["text_field"]
        newComment = Comments(writer = currentUser, text = message, listing = listingData)
        newComment.save()
    return HttpResponseRedirect(reverse("auctions:listing", kwargs={'itemID':itemID}))

@login_required(login_url= 'auctions:login')
def add(request):
    categories = Category.objects.all()
    owner = request.user
    form = createListing()
    if request.method == "POST":
        img = request.FILES["img"]
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        category = request.POST["categories"]
        listing = Listing(title=title, description=description, img=img, owner=owner, categories = Category.objects.get(id=category), price = price)
        listing.save()
        initial = Bid(bid_offer = listing.price, listing_offer = listing, bid_owner=owner) #initial price of bid
        initial.save()

    context = {'owner': owner, "categories":categories, "form":form}
    return render(request, "auctions/add.html", context)

@login_required(login_url= 'auctions:login')
def viewListing(request, itemID):
    listing = Listing.objects.get(id = itemID)  #Gets the relevant post
    form = bidForm()

    isListinginWatchlist = request.user in listing.watchlist.all() #returns the boolean if user in watchlist
        
    if request.method == "POST" and 'place' in request.POST: #BID FORM
        new_bid = request.POST.get("new_bid")
        f = Bid(bid_offer = new_bid, listing_offer = listing, bid_owner = request.user)
        f.save()
        return HttpResponseRedirect(f'./{itemID}')

    cat = listing.categories
    bid = Bid.objects.filter(listing_offer_id=itemID).order_by("bid_offer").values()
    last_bid = bid.last()# the last value of sorted list of bids
    bid_offer = last_bid["bid_offer"] # gets the max value of bid offers   
    bid_owner = User.objects.filter(id=last_bid['bid_owner_id'])

    for i in bid_owner:# gets username without brackets
        bid_owner = i
        
### ACCEPT FUNCTION
    if request.method == "POST" and 'accept' in request.POST:
        listing.isActive = False
        listing.save()
        return HttpResponseRedirect(f'./{itemID}')
    allComments = Comments.objects.filter(listing = listing)
    message = f"Last bid was offered by {bid_owner} in amount of {bid_offer}$ for the {listing.title}"
        
    context = {'Listing': listing, 'title': listing.title, 'description': listing.description,
                    'owner':listing.owner, 'category': cat, 'image':listing.img, 'bid':message, 'itemID': itemID, 
                    'form': form, 'isActive':listing.isActive, 'isWatching': isListinginWatchlist, 'comments':allComments}

    return render(request, "auctions/listing.html", context)

def removeWatchlist(request,itemID):
    listing = Listing.objects.get(id = itemID)
    currentUser = request.user
    listing.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("auctions:listing", kwargs={'itemID':itemID}))
 
def addWatchlist(request,itemID):
    listing = Listing.objects.get(id = itemID)
    currentUser = request.user
    listing.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("auctions:listing", kwargs={'itemID':itemID}))

@login_required
def watchlist(request):
    currentUser = request.user
    listing = currentUser.userTo.all()
    context = {'listings':listing}
    return render(request, 'auctions/watchlist.html',context)
 