# cars/models.py
from django.db import models
from django.urls import reverse
from django.conf import settings

class CarBrand(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Марка'
    )
    logo = models.ImageField(
        upload_to='car_brands/',
        blank=True,
        null=True,
        verbose_name='Логотип'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    brand = models.ForeignKey(
        CarBrand,
        on_delete=models.CASCADE,
        related_name='models',
        verbose_name='Марка'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Модель'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        ordering = ['name']
        unique_together = ['brand', 'name']
    
    def __str__(self):
        return f'{self.brand.name} {self.name}'

class Car(models.Model):
    
    BODY_TYPE_CHOICES = [
        ('sedan', 'Седан'),
        ('hatchback', 'Хэтчбек'),
        ('wagon', 'Универсал'),
        ('coupe', 'Купе'),
        ('convertible', 'Кабриолет'),
        ('suv', 'Внедорожник'),
        ('crossover', 'Кроссовер'),
        ('pickup', 'Пикап'),
        ('minivan', 'Минивэн'),
        ('other', 'Другое'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('gasoline', 'Бензин'),
        ('diesel', 'Дизель'),
        ('hybrid', 'Гибрид'),
        ('electric', 'Электричество'),
        ('gas', 'Газ'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Механическая'),
        ('automatic', 'Автоматическая'),
        ('cvt', 'Вариатор'),
        ('robot', 'Робот'),
    ]
    
    DRIVE_TYPE_CHOICES = [
        ('front', 'Передний'),
        ('rear', 'Задний'),
        ('all', 'Полный'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у'),
        ('damaged', 'Требует ремонта'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('sold', 'Продано'),
        ('inactive', 'Неактивно'),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Владелец'
    )
    brand = models.ForeignKey(
        CarBrand,
        on_delete=models.CASCADE,
        verbose_name='Марка'
    )
    model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        verbose_name='Модель'
    )
    
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска'
    )
    body_type = models.CharField(
        max_length=20,
        choices=BODY_TYPE_CHOICES,
        verbose_name='Тип кузова'
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE_CHOICES,
        verbose_name='Тип топлива'
    )
    engine_volume = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='Объем двигателя (л)'
    )
    engine_power = models.PositiveIntegerField(
        verbose_name='Мощность (л.с.)'
    )
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        verbose_name='Коробка передач'
    )
    drive_type = models.CharField(
        max_length=10,
        choices=DRIVE_TYPE_CHOICES,
        verbose_name='Привод'
    )
    mileage = models.PositiveIntegerField(
        verbose_name='Пробег (км)'
    )
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        verbose_name='Состояние'
    )
    
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена (руб.)'
    )
    is_negotiable = models.BooleanField(
        default=True,
        verbose_name='Торг уместен'
    )
    
    color = models.CharField(
        max_length=50,
        verbose_name='Цвет'
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
        verbose_name='VIN номер'
    )
    license_plate = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Гос. номер'
    )
    
    description = models.TextField(
        verbose_name='Описание'
    )
    location = models.CharField(
        max_length=100,
        verbose_name='Местоположение'
    )
    contact_phone = models.CharField(
        max_length=17,
        verbose_name='Контактный телефон'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров'
    )
    
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.brand.name} {self.model.name} {self.year}'
    
    def get_absolute_url(self):
        return reverse('cars:car_detail', kwargs={'pk': self.pk})
    
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_main_image(self):
        """Получить главное изображение"""
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image
        return self.images.first()

class CarImage(models.Model):
    """Изображения автомобиля"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Автомобиль'
    )
    image = models.ImageField(
        upload_to='car_images/',
        verbose_name='Изображение'
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Главное фото'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Изображение автомобиля'
        verbose_name_plural = 'Изображения автомобилей'
        ordering = ['-is_main', 'created_at']
    
    def __str__(self):
        return f'Фото {self.car}'

class CarFeature(models.Model):
    """Дополнительные опции автомобиля"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название опции'
    )
    category = models.CharField(
        max_length=50,
        verbose_name='Категория'
    )
    
    class Meta:
        verbose_name = 'Опция автомобиля'
        verbose_name_plural = 'Опции автомобилей'
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name

class CarFeatureRelation(models.Model):
    """Связь автомобиля с опциями"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='car_features'
    )
    feature = models.ForeignKey(
        CarFeature,
        on_delete=models.CASCADE
    )
    
    class Meta:
        unique_together = ['car', 'feature']
        verbose_name = 'Опция автомобиля'
        verbose_name_plural = 'Опции автомобилей'

class CarView(models.Model):
    """Просмотры автомобилей (для аналитики)"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='car_views'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Просмотр автомобиля'
        verbose_name_plural = 'Просмотры автомобилей'