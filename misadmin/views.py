from generic.views import GenericListView
from django.shortcuts import render, redirect

class DashboardView(GenericListView):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')