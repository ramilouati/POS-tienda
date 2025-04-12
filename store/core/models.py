from django.db import models


class Bussiness(models.Model):
    QUINCAILLERIE = 0
    MEUBLES = 1
    DECORATION = 2
    ELECTRONIQUE = 3
    DETAILLEUR = 4
    ARTISANAT = 5
    AGRICOLES = 6
    AUTRES = 7
    BUSSINESS_TYPE = [
        (QUINCAILLERIE, 'Quincaillerie'),
        (MEUBLES, 'Meubles'),
        (DECORATION, 'Decoration'),
        (ELECTRONIQUE, 'Electronique'),
        (DETAILLEUR, 'Détailleur'),
        (ARTISANAT, 'Artisanat'),
        (AGRICOLES, 'Agriculture'),
        (AUTRES, 'Autres'),
    ]
    matricule_fiscale = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=BUSSINESS_TYPE)

    def __str__(self):
        return self.matricule_fiscale