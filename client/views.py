from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


from client.forms import ClientForm
from client.models import Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client
    template_name = 'client/client_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ClientDetailView(DetailView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_detail.html'


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client:view_client', args=[self.object.pk])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:client')

