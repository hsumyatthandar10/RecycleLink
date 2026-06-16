from django import forms
from django.core.exceptions import ValidationError
from .models import ProductPhotoBuy, ProductPhotoSell


class ProductPhotoBuyForm(forms.ModelForm):
    class Meta:
        model = ProductPhotoBuy
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        is_required = cleaned_data.get("is_required")

        # Validate total number of photos for a product
        total_photos = ProductPhotoBuy.objects.filter(product=product).exclude(pk=self.instance.pk).count()
        if total_photos >= 8:
            raise ValidationError("You can only upload up to 8 photos for this product on the buy page.")

        # Validate required photos for a product
        if is_required:
            required_photos = ProductPhotoBuy.objects.filter(product=product, is_required=True).exclude(pk=self.instance.pk).count()
            if required_photos >= 2:
                raise ValidationError("You can only mark 2 photos as required.")


class ProductPhotoSellForm(forms.ModelForm):
    class Meta:
        model = ProductPhotoSell
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")

        # Validate total number of photos for a product
        total_photos = ProductPhotoSell.objects.filter(product=product).exclude(pk=self.instance.pk).count()
        if total_photos >= 2:
            raise ValidationError("You can only upload up to 2 photos for this product on the sell page.")
