from django.contrib import admin
from django.urls import path, include
from notes.views import (
    NoteListView, NoteDetailView, NoteCreateView,
    NoteUpdateView, NoteDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', NoteListView.as_view(), name='note_list'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('note/new/', NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('', include('notes.urls'))
]
