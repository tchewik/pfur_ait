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

            roots = np.roots([a, b, c])
            if len(roots) == 1:
                roots *= 2
            if len(roots) == 2:
                if type(roots[0]) != np.complex128:

                    data['x1'], data['x2'] = roots
                    x = np.arange(data['x1']-5, data['x2']+5, 0.1)
                    y = plots.get_str_quadr_y(a, b, c)
                    data['plot'] = plots.plot_function(x=x, f_str=y, quadratic=True)

                else:
                    data['complex_roots_exception'] = 'The roots are complex; not allowed.'

            return render(request, template_name, data)

    return render(request, template_name)


def plot_view(request):
    template_name = 'plot.html'

    if request.method == 'POST':
        form = forms.SendFunctionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            x = np.arange(data['x0'], data['x1']+min(abs(data['x1'] - data['x0']), data['step']), data['step'])
            y = data['function'].replace(' ', '')
            data['function'] = y
            data['plot'] = plots.plot_function(x=x, f_str=y)

            return render(request, template_name, data)

    return render(request, template_name)