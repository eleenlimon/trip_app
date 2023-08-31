from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from typing import List
from .models import Trip, Note
from django import forms


# Create your views here.
class HomeView(TemplateView):
    template_name = "trip/index.html"


def trips_list(request):
    trips = Trip.objects.filter(owner=request.user)  # this filter/owner -to display only the users trips
    context = {
        'trips': trips
    }
    return render(request, "trip/trip_list.html", context)


class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']

    # template named model_form.html

    def form_valid(self, form):  # this form is submitted each time new img is added/ VALID to save to db
        # the form is the class TripCreateView(all the fields) that is being passed in w correct owner
        #  add owner field = logged in user
        form.instance.owner = self.request.user
        return super().form_valid(form)
    # passing in the form with the owner now


class TripDetailView(DetailView):
    model = Trip

    # data stored on Trip in models.py --also have the Notes data by
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context['object']  # getting all data associated with that img
        notes = trip.notes.all()  # able to call it notes bc in models.py related name is notes
        context['notes'] = notes
        return context
        # this will give us the notes only associated with that img
    ### template named trip_detail.html


class NoteDetailView(DetailView):
    model = Note


# allows us to see the Note details, makes template note_detail.html

class NoteListView(ListView):
    model = Note  # keep in mind dont want to return all the notes just user img notes

    def get_queryset(self):
        queryset = Note.objects.filter(trip__owner=self.request.user)
        return queryset
    # overding queryset w/ own variable to-> trip__owner gives access to model Trip object(owner)
    # template is model_list.html


class NoteCreateView(CreateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = '__all__'  # allows you to get all the fields in Note

    # template is model_form.html

    def get_form(self):
        form = super(NoteCreateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)  # gets the trips only for logged in user
        form.fields['trip'].queryset = trips  # modifing the to give a dropdown of only user's img
        return form
    # able to modify these terms to do what we would like ***keyyy


class NoteUpdateView(UpdateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = '__all__'

    def get_form(self):
        form = super(NoteUpdateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form


class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')
    # no template needed -> send a post request to this url


class TripUpdateView(UpdateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']
    # template is same as tripcreateview -> trip_form.html


class TripDeleteView(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    # no template needed
