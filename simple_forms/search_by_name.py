from django import forms


class SearchByNameForm(forms.Form):
    name = forms.CharField(
        max_length=10,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "text search-input",
                "placeholder": "Searching by name"
            }
        )
    )
