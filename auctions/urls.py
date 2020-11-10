from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"), 
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/open", views.openclose, name="openclose"),
    path("listing/<int:listing_id>/watch", views.togglewatch, name="togglewatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addlisting", views.addlisting, name="addlisting"),
    path("listing/<int:listing_id>/addcomment", views.addcomment, name="addcomment"),
    path("listing/<int:listing_id>/addbid", views.addbid, name="addbid"),
]
