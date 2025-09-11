from django import forms
from .models import Delivery, DELIVERY_TYPES
from decimal import Decimal, InvalidOperation

class DeliveryForm(forms.ModelForm):
    delivery_date = forms.DateField(
        label="Data dostawy",
        input_formats=["%d.%m.%Y"],
        widget=forms.DateInput(attrs={"placeholder":"DD.MM.RRRR"})
    )
    delivery_type = forms.ChoiceField(label="Typ dostawy", choices=DELIVERY_TYPES)

    # HU jako stringi -> czyścimy na Decimal w clean_*
    hu_paleta   = forms.CharField(label="Paleta",   required=False)
    hu_karton   = forms.CharField(label="Karton",   required=False)
    hu_kontener = forms.CharField(label="Kontener", required=False)

    class Meta:
        model = Delivery
        fields = [
            "company",
            "delivery_date","delivery_type",
            "hu_paleta","hu_karton","hu_kontener",
            "driver_name","driver_phone","truck_no","trailer_no",
            "order_no","attachment",
        ]

    def _clean_decimal(self, field):
        raw = (self.cleaned_data.get(field) or "").strip().replace("\u00a0","").replace(" ","")
        if raw == "":
            return Decimal("0")
        if "," in raw:
            raw = raw.replace(".", "").replace(",", ".")
        try:
            val = Decimal(raw)
        except (InvalidOperation, ValueError):
            raise forms.ValidationError("Podaj liczbę (np. 12,5).")
        if val < 0:
            raise forms.ValidationError("Wartość nie może być ujemna.")
        return val

    def clean_hu_paleta(self):   return self._clean_decimal("hu_paleta")
    def clean_hu_karton(self):   return self._clean_decimal("hu_karton")
    def clean_hu_kontener(self): return self._clean_decimal("hu_kontener")

    def clean_driver_phone(self):
        s = (self.cleaned_data.get("driver_phone") or "")
        return s.replace(" ","").replace("-","").replace("(","").replace(")","").replace(".","")

class DeliveryEditForm(DeliveryForm):
    remove_attachment = forms.BooleanField(label="Usuń obecny załącznik", required=False)
