# dashboard/forms.py
from django import forms
from django.utils import timezone
import calendar

class MonthSelectorForm(forms.Form):
    # Generate year choices: last 5 years up to the current year
    current_year = timezone.localdate().year
    YEAR_CHOICES = [(year, str(year)) for year in range(current_year - 4, current_year + 1)]
    
    # Generate month choices: 1-12 mapped to month names
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]

    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=current_year,
        label="Año"
    )
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        initial=timezone.localdate().month, # Default to current month
        label="Mes"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If you want to use crispy forms or add specific Bootstrap classes,
        # you can modify widget attributes here. For example:
        # self.fields['year'].widget.attrs.update({'class': 'form-select form-select-sm'})
        # self.fields['month'].widget.attrs.update({'class': 'form-select form-select-sm'})
