from django import forms
from pos.models import Sales
from datetime import datetime
from django import forms

from purchase.models import *
MONTH_NAMES = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre'

]


MONTH_CHOICES = [(str(i), month) for i, month in enumerate(MONTH_NAMES, 1)]


DAYS_OF_WEEK = {
    'Monday': 'Lundi',
    'Tuesday': 'Mardi',
    'Wednesday': 'Mérecredi',
    'Thursday': 'Jeudi',
    'Friday': 'Vendredi',
    'Saturday': 'Samedi',
    'Sunday': 'Dimanche',
}

class SalesReportForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    customer = forms.CharField(max_length=100, required=False)


class YearMonthForm(forms.Form):
    year = forms.IntegerField(label="Année", min_value=1900, max_value=2100)
    month = forms.ChoiceField(label="Mois", choices=MONTH_CHOICES)


class YearForm(forms.Form):
    year = forms.IntegerField(label="Année", min_value=1900, max_value=2100)


class DayForm(forms.Form):
    year = forms.IntegerField(label="Année", min_value=1900, max_value=2100)
    month = forms.ChoiceField(label="Mois", choices=MONTH_CHOICES)
    day = forms.IntegerField(label="Jour", min_value=1, max_value=31)


class DateRangeForm(forms.Form):
    fecha_desde = forms.DateField(label="Date à partir de", widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_hasta = forms.DateField(label="Date à", widget=forms.DateInput(attrs={'type': 'date'}))


class ReportForm(forms.Form):
    pass

class MonthReportForm(forms.Form):
    year = forms.IntegerField(label='Année', min_value=1900, max_value=datetime.now().year)
    month = forms.IntegerField(label='Mois', min_value=1, max_value=12)

class DayReportForm(forms.Form):
    year = forms.IntegerField(label='Année', min_value=1900, max_value=datetime.now().year)
    month = forms.IntegerField(label='Mois', min_value=1, max_value=12)
    day = forms.IntegerField(label='Día', min_value=1, max_value=31)

class PurchaseReportForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)


class YearReportForm(forms.Form):
    current_year = datetime.now().year
    YEAR_CHOICES = [(year, year) for year in range(current_year - 10, current_year + 1)]

    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label="Seleccione el Año", widget=forms.Select)

class MonthYearReportForm(forms.Form):
    year = forms.IntegerField(min_value=2000, max_value=timezone.now().year, label='Año')
    month = forms.IntegerField(min_value=1, max_value=12, label='Mois')

class DayMonthYearReportForm(forms.Form):
    year = forms.IntegerField(min_value=2000, max_value=timezone.now().year, label='Año')
    month = forms.IntegerField(min_value=1, max_value=12, label='Mois')
    day = forms.IntegerField(min_value=1, max_value=31, label='Día')  # Nota: No valida días específicos para cada mes

class DayTramoForm(forms.Form):
    start_year = forms.IntegerField(label="Début de l'année", min_value=2023)
    start_month = forms.ChoiceField(label='Début de Mois', choices=[
        ('', 'Mois'),
        (1, 'Janvier'),
        (2, 'Février'),
        (3, 'Mars'),
        (4, 'Avril'),
        (5, 'Mai'),
        (6, 'Juin'),
        (7, 'Juillet'),
        (8, 'Août'),
        (9, 'Septembre'),
        (10, 'Octobre'),
        (11, 'Novembre'),
        (12, 'Décembre'),
    ])
    start_day = forms.IntegerField(label='Jour de départ', min_value=1, max_value=31)

    end_year = forms.IntegerField(label="Fin d'année", min_value=2023)
    end_month = forms.ChoiceField(label='Fin de Mois', choices=[
         ('', 'Mois'),
        (1, 'Janvier'),
        (2, 'Février'),
        (3, 'Mars'),
        (4, 'Avril'),
        (5, 'Mai'),
        (6, 'Juin'),
        (7, 'Juillet'),
        (8, 'Août'),
        (9, 'Septembre'),
        (10, 'Octobre'),
        (11, 'Novembre'),
        (12, 'Décembre'),
    ])
    end_day = forms.IntegerField(label='Fin du jour', min_value=1, max_value=31)

