from django import forms
from .models import Listing, Review


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ListingForm(forms.ModelForm):
    images = MultipleImageField(
        required=False,
        label='Rasmlar'
    )

    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'listing_type',
            'property_type',
            'price',
            'price_currency',
            'is_negotiable',
            'area',
            'rooms',
            'floor',
            'total_floors',
            'address',
            'latitude',
            'longitude',
            'region',
            'district',
            'category',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E\'lon sarlavhasi'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Batafsil tavsif...'
            }),
            'listing_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'property_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Narx'
            }),
            'price_currency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maydon (m²)'
            }),
            'rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Xonalar soni'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qavat'
            }),
            'total_floors': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Umumiy qavatlar'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Manzil'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '41.2995'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '69.2401'
            }),
            'region': forms.Select(attrs={
                'class': 'form-select'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_negotiable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} yulduz') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Sharh yozing...'
            }),
        }