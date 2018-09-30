from django import forms


class SendStringForm(forms.Form):
    string = forms.CharField()


class SendEquationForm(forms.Form):
    a = forms.FloatField(initial=0)
    b = forms.FloatField(initial=0)
    c = forms.FloatField(initial=0)


class SendFunctionForm(forms.Form):
    function = forms.CharField()
    x0 = forms.FloatField()
    x1 = forms.FloatField()
    step = forms.FloatField(min_value=0.01)
