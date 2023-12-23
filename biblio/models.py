from django.db import models
from datetime import datetime


# Create your models here.
class Livre(models.Model):
    nom= models.CharField(max_length=255)
    categorie= models.CharField(max_length=255)
    auteur= models.CharField(max_length=255)
    synopsis= models.CharField(max_length=1000)
    prix=models.FloatField()
    qt= models.IntegerField()
    pic = models.ImageField(null=True,blank=True, upload_to='images/')
    
    def __str__(self):
        return str(self.nom)
    

    
class Manager(models.Model):
    nom= models.CharField(max_length=255)
    prenom= models.CharField(max_length=255)
    email= models.EmailField()
    password= models.CharField(max_length=255)
    
    
class Adherent(models.Model):
    nom= models.CharField(max_length=255)
    prenom= models.CharField(max_length=255)
    email= models.EmailField(default='default@gmail.com')
    password= models.CharField(max_length=255,default='default')
    
    def __str__(self):
        return str(self.nom)    
    
    
class empreinte(models.Model):
    liv_id=models.ForeignKey(Livre, on_delete=models.CASCADE)
    man_id=models.ForeignKey(Manager, on_delete=models.CASCADE)
    ad_id=models.ForeignKey(Adherent, on_delete=models.CASCADE)
    begin=models.DateField(default=datetime.now)
    end=models.DateField()
    returned=models.BooleanField(default=False)
    
    def nom_liv(self):
        return self.liv_id.nom
    def nom_man(self):
        return self.man_id.nom
    def nom_ad(self):
        return self.ad_id.nom    

class transaction(models.Model):
    liv_id=models.ForeignKey(Livre, on_delete=models.CASCADE)
    man_id=models.ForeignKey(Manager, on_delete=models.CASCADE)
    ad_id=models.ForeignKey(Adherent, on_delete=models.CASCADE)
    montant=models.FloatField()
    date=models.DateField(default=datetime.now)
    qt=models.IntegerField()
    confirmed=models.BooleanField(default=False)

    
    def nom_liv(self):
        return self.liv_id.nom
    def nom_man(self):
        return self.man_id.nom
    def nom_ad(self):
        return self.ad_id.nom   


    