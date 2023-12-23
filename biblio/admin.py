from django.contrib import admin
from .models import Livre,Manager,Adherent,empreinte,transaction

# Register your models here.

class Livreadmin(admin.ModelAdmin):
    list_display=('id','nom','categorie','auteur','synopsis','prix','qt','pic')
    search_fields=('id','nom','categorie','auteur','synopsis','prix','qt','pic')
    
class Manageradmin(admin.ModelAdmin):
    list_display=('id','nom','prenom','email','password')
    search_fields=('id','nom','prenom','email','password')

class Adherentadmin(admin.ModelAdmin):
    list_display=('id','nom','prenom','email','password')
    search_fields=('id','nom','prenom','email','password')
    
class empreinteadmin(admin.ModelAdmin):
    list_display=('id','nom_liv','nom_man','nom_ad','begin','end','returned')
    search_fields=('id','nom_liv','nom_man','ad_id','begin','end','returned')
    
class transactioneadmin(admin.ModelAdmin):
    list_display=('id','nom_liv','nom_man','nom_ad','montant','date','qt','confirmed')
    search_fields=('id','nom_liv','nom_man','nom_ad','montant','date','qt','confirmed')


admin.site.register(Livre,Livreadmin)
admin.site.register(Manager,Manageradmin)
admin.site.register(Adherent,Adherentadmin)
admin.site.register(empreinte,empreinteadmin)
admin.site.register(transaction,transactioneadmin)