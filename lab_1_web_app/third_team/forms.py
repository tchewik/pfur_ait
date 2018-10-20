from django import forms


class SendStringForm(forms.Form):
    string = forms.CharField(min_length=1, max_length=500)


class SendEquationForm(forms.Form):
    a = forms.FloatField(initial=0, min_value=-100, max_value=100)
    b = forms.FloatField(initial=0, min_value=-100, max_value=100)
    c = forms.FloatField(initial=0, min_value=-100, max_value=100)


class SendFunctionForm(forms.Form):
    function = forms.CharField()
    x0 = forms.FloatField(min_value=-1000, max_value=1000)
    x1 = forms.FloatField(min_value=-100, max_value=100)
    step = forms.FloatField(min_value=0.01, max_value=50)
