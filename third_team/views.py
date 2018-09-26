import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, render_to_response
import numpy as np


from . import plots
from . import forms

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


def reverse_view(request):
    template_name = 'reverse.html'

    if request.method == 'POST':
        form = forms.SendStringForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            string = data['string']
            data['reversed_string'] = ''.join(reversed(list(string)))

            return render(request, template_name, data)

    return render(request, template_name)


def solve_eq_view(request):
    template_name = 'solve_equation.html'

    if request.method == 'POST':
        form = forms.SendEquationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            a = data['a']
            b = data['b']
            c = data['c']
            data['x1'], data['x2'] = np.roots([a, b, c])
            x = np.arange(data['x1']-5, data['x2']+5, 0.1)

            y = ''
            y += str(a) * (a not in [0, 1]) + 'x^2' * (a != 0)
            y += str(b) * (b not in [0, 1]) + 'x' * (b != 0)
            y += str(c) * (c not in [0, 1])
            data['plot'] = plots.plot_function(x=x, f_str=y, quadratic=True)

            return render(request, template_name, data)

    return render(request, template_name)


def plot_view(request):
    template_name = 'plot.html'

    if request.method == 'POST':
        form = forms.SendFunctionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            x = np.arange(data['x0'], data['x1'], data['step'])
            y = data['function'].replace(' ', '')
            data['function'] = y
            data['plot'] = plots.plot_function(x=x, f_str=y)

            return render(request, template_name, data)

    return render(request, template_name)