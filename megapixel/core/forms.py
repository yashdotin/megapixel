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


class BulkImageUploadForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(),
        required=True
    )
