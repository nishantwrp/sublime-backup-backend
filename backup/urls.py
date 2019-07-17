from django.urls import path,include
from .views import *
urlpatterns = [
   path('snippets/upload/', SnippetsUpdateView.as_view()),
   path('snippets/', SnippetsListView.as_view()),
   path('snippets/delete/', SnippetsDeleteView.as_view()),
   path('snippets/<str:id>/',getSnippet),
]
