# cars/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Car, CarImage, CarBrand, CarModel, CarFeature

class CarForm(forms.ModelForm):
    """Форма для добавления/редактирования автомобиля"""
    
    features = forms.ModelMultipleChoiceField(
        queryset=CarFeature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Дополнительные опции'
    )
    
    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'year', 'body_type', 'fuel_type',
            'engine_volume', 'engine_power', 'transmission', 'drive_type',
            'mileage', 'condition', 'price', 'is_negotiable', 'color',
            'vin', 'license_plate', 'description', 'location', 'contact_phone'
        ]
        
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control', 'id': 'id_brand'}),
            'model': forms.Select(attrs={'class': 'form-control', 'id': 'id_model'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2024}),
            'body_type': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'engine_volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'engine_power': forms.NumberInput(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'drive_type': forms.Select(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_negotiable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если выбрана марка, фильтруем модели
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = CarModel.objects.filter(brand_id=brand_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['model'].queryset = self.instance.brand.models.all()
        else:
            self.fields['model'].queryset = CarModel.objects.none()

class CarImageForm(forms.ModelForm):
    """Форма для загрузки изображений автомобиля"""
    
    class Meta:
        model = CarImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*',
                'multiple': True
            }),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Формсет для множественной загрузки изображений
CarImageFormSet = inlineformset_factory(
    Car, 
    CarImage, 
    form=CarImageForm,
    extra=5,
    max_num=10,
    can_delete=True
)

class CarSearchForm(forms.Form):
    """Форма поиска автомобилей"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по марке, модели...'
        }),
        label='Поиск'
    )
    
    brand = forms.ModelChoiceField(
        queryset=CarBrand.objects.all(),
        required=False,
        empty_label="Все марки",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'search_brand'}),
        label='Марка'
    )
    
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(),
        required=False,
        empty_label="Все модели",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'search_model'}),
        label='Модель'
    )
    
    year_from = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'От',
            'min': 1900,
            'max': 2024
        }),
        label='Год от'
    )
    
    year_to = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'До',
            'min': 1900,
            'max': 2024
        }),
        label='Год до'
    )
    
    price_from = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'От'
        }),
        label='Цена от'
    )
    
    price_to = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'До'
        }),
        label='Цена до'
    )
    
    body_type = forms.ChoiceField(
        choices=[('', 'Любой')] + Car.BODY_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип кузова'
    )
    
    fuel_type = forms.ChoiceField(
        choices=[('', 'Любой')] + Car.FUEL_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип топлива'
    )
    
    transmission = forms.ChoiceField(
        choices=[('', 'Любая')] + Car.TRANSMISSION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Коробка передач'
    )
    
    condition = forms.ChoiceField(
        choices=[('', 'Любое')] + Car.CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Состояние'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = CarModel.objects.filter(brand_id=brand_id)
            except (ValueError, TypeError):
                pass