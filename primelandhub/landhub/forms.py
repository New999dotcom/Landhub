from django import forms
from .models import property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = property
        fields = [
            'name', 'phone', 'place', 'propertytype', 'prop', 'price', 'description', 
            'status', 'date', 'image', 'document', 'bedrooms', 'bathrooms', 
            'area_sqft', 'is_furnished', 'parking_space'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    # Custom validations
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not str(phone).isdigit() or len(str(phone)) < 10 or len(str(phone)) > 15:
            raise forms.ValidationError("Phone number must be 10-15 digits.")
        return phone

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_area_sqft(self):
        area = self.cleaned_data['area_sqft']
        if area <= 0:
            raise forms.ValidationError("Area must be greater than zero.")
        return area

    def clean_bedrooms(self):
        bedrooms = self.cleaned_data['bedrooms']
        if bedrooms < 1:
            raise forms.ValidationError("Bedrooms must be at least 1.")
        return bedrooms

    def clean_bathrooms(self):
        bathrooms = self.cleaned_data['bathrooms']
        if bathrooms < 1:
            raise forms.ValidationError("Bathrooms must be at least 1.")
        return bathrooms