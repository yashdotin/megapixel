from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-black outline-none",
            "placeholder": "Your full name"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-black outline-none",
            "placeholder": "your@email.com"
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-black outline-none",
            "rows": 4,
            "placeholder": "Tell us about your project..."
        })
    )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_clean = super().clean
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return [single_clean(item, initial) for item in data]
        return [single_clean(data, initial)]


class BulkImageUploadForm(forms.Form):
    images = MultipleFileField(required=True)


class BulkCategoryImageUploadForm(forms.Form):
    category = forms.ChoiceField(choices=[
        ('wedding', 'Wedding'),
        ('prewedding', 'Pre-Wedding'),
        ('cinematography', 'Cinematography'),
        ('babyshoot', 'Baby Shoot'),
        ('advertisement', 'Advertisement'),
        ('corporate', 'Corporate Shoot'),
    ])
    images = MultipleFileField(required=True)