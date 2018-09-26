from django import forms


class SendStringForm(forms.Form):
    string = forms.CharField()


class SendEquationForm(forms.Form):
    a = forms.FloatField(initial=0)
    b = forms.FloatField(initial=0)
    c = forms.FloatField(initial=0)


class SendFunctionForm(forms.Form):
    function = forms.CharField()
    x0 = forms.IntegerField()
    x1 = forms.IntegerField()
    step = forms.FloatField()
