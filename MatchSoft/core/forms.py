from django import forms

class AnswerForm(forms.Form):
    choice_label = forms.ChoiceField(choices=[(c, c) for c in 'ABCD'])
