# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.conf import settings
from django.db import models
from core.models import TimestampedModel

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

@python_2_unicode_compatible
class Perimeter(TimestampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    color = models.CharField(max_length=200)
    perimeter = models.CharField(max_length=200)
    major = models.IntegerField()
    moderate = models.IntegerField()
    minor = models.IntegerField()
    total_budget = models.IntegerField(default=0)
    spent_budget = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('change_status', 'Change vulnerability status'),
        )

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class URL(TimestampedModel):
    perimeter = models.ForeignKey('Perimeter', on_delete=models.CASCADE, related_name='urls')
    url = models.TextField()

    def __str__(self):
        return self.url

@python_2_unicode_compatible
class Account(TimestampedModel):
    perimeter = models.ForeignKey('Perimeter', on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(TimestampedModel):
    perimeter = models.ForeignKey('Perimeter', on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Vulnerability(TimestampedModel):
    VULNERABILITY_STATE_CHOICES = (
        ('O', 'Open'),
        ('R', 'Retry'),
        ('C', 'Closed'),
    )
    VULNERABILITY_THEME_CHOICES = (
        ('Infrastructure et réseau', 'Infrastructure et réseau'),
        ('Sécurisation des plateformes', 'Sécurisation des plateformes'),
        ('Authentification et chiffrement', 'Authentification et chiffrement'),
        ('Gestion des sessions', 'Gestion des sessions'),
        ('Contrôle des autorisations', 'Contrôle des autorisations'),
        ('Traitement des paramètres', 'Traitement des paramètres'),
        ('Conformité légale', 'Conformité légale'),
    )
    VULNERABILITY_PORTEUR_CHOICES = (
        ('A', 'Architect'),
        ('D', 'Developer'),
        ('E', 'Exploitant'),
    )

    VULNERABILITY_ATTACK_VECTOR_CHOICES = (
        ('0.2', 'Physical'),
        ('0.55', 'Local'),
        ('0.62', 'Adjacent Network'),
        ('0.85', 'Network'),
    )

    VULNERABILITY_ATTACK_COMPLEXITY_CHOICES = (
        ('0.77', 'Low'),
        ('0.44', 'High'),
    )

    VULNERABILITY_PRIVILEGES_REQUIRED_CHOICES = (
        ('0.85', 'None'),
        ('0.62', 'Low'),
        ('0.27', 'High'),
    )

    VULNERABILITY_USER_INTERACTION_CHOICES = (
        ('0.85', 'None'),
        ('0.62', 'Required'),
    )

    VULNERABILITY_CONFIDENTIALITY_CHOICES = (
        ('0', 'None'),
        ('0.22', 'Low'),
        ('0.56', 'High'),
    )

    VULNERABILITY_AVAILABILITY_CHOICES = (
        ('0', 'None'),
        ('0.22', 'Low'),
        ('0.56', 'High'),
    )

    VULNERABILITY_INTEGRITY_CHOICES = (
        ('0', 'None'),
        ('0.22', 'Low'),
        ('0.56', 'High'),
    )

    VULNERABILITY_SCOPE_CHOICES = (
        ('U', 'Unchanged'),
        ('C', 'Changed'),
    )

    VULNERABILITY_PRIORITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    )
    VULNERABILITY_CRITICALITY = (
        ('L', 'Minor'),
        ('M', 'Moderate'),
        ('H', 'Major'),
    )

    perimeter = models.ForeignKey('Perimeter', on_delete=models.CASCADE, related_name='vulnerabilities')
    name = models.CharField(max_length=200)
    description = models.TextField()
    mode_operatoire = models.TextField(default="")
    theme = models.CharField(max_length=40, choices=VULNERABILITY_THEME_CHOICES)
    state = models.CharField(max_length=2, choices=VULNERABILITY_STATE_CHOICES, default='O')
    priority = models.CharField(max_length=2, choices=VULNERABILITY_PRIORITY_CHOICES, default='L')
    porteur = models.CharField(max_length=2, choices=VULNERABILITY_PORTEUR_CHOICES)
    complexity = models.CharField(max_length=1, choices=VULNERABILITY_ATTACK_COMPLEXITY_CHOICES, default='N')
    privileges = models.CharField(max_length=1, choices=VULNERABILITY_PRIVILEGES_REQUIRED_CHOICES, default='N')
    interaction = models.CharField(max_length=1, choices=VULNERABILITY_USER_INTERACTION_CHOICES, default='N')
    confidentiality = models.CharField(max_length=1, choices=VULNERABILITY_CONFIDENTIALITY_CHOICES, default='N')
    availability = models.CharField(max_length=1, choices=VULNERABILITY_AVAILABILITY_CHOICES, default='N')
    integrity = models.CharField(max_length=1, choices=VULNERABILITY_INTEGRITY_CHOICES, default='N')
    scope = models.CharField(max_length=1, choices=VULNERABILITY_SCOPE_CHOICES, default='U')
    vector = models.CharField(max_length=5, choices=VULNERABILITY_ATTACK_VECTOR_CHOICES )
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)
    note =  models.DecimalField(max_digits=2, decimal_places=1)
    criticality = models.CharField(max_length=1, choices=VULNERABILITY_CRITICALITY, default='L')

    def __str__(self):
        return 'VLN{id} : {name}'.format(id=self.id, name=self.name)

@python_2_unicode_compatible
class Comment(TimestampedModel):
    vulnerability = models.ForeignKey('Vulnerability', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
on_delete=models.SET(get_sentinel_user))
    description = models.TextField()

    def __str__(self):
        return '%s - [%s] %s' % (self.vulnerability, self.author, self.description)

class Video(TimestampedModel):
    vulnerability = models.ForeignKey('Vulnerability', on_delete=models.CASCADE, related_name='videos', null=True)
    name= models.CharField(max_length=500)
    description= models.TextField()
    file= models.FileField(upload_to='videos/', null=True, verbose_name="")
