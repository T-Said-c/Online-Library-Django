from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,Http404
from .models import Livre,Manager,Adherent,empreinte,transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
import random


# Create your views here.
def index(request):
    livres=Livre.objects.all()
    output=""
    for l in livres:
        output+= l.nom +" "+ l.categorie +" "+ l.auteur +" "+ l.synopsis +" "+ str(l.prix) +" "+ str(l.qt)
    return render(request,'bib/index.html',{'livres':livres})

@csrf_exempt
def home(request,man_id):
 manager = get_object_or_404(Manager,id=man_id)  
 if request.method== "POST":
    data =request.POST
    nom = data.get('nom')
    prenom = data.get('prenom')
    password = data.get('password')
    manager.nom = nom
    manager.prenom = prenom
    manager.password = password
    manager.save()
 return render(request,"bib/home.html",{"manager":manager})


@csrf_exempt
def login(request):
 if request.method== "POST":
        data =request.POST
        managers=Manager.objects.all()
        mail = data.get('email')
        mdp = data.get('password')
        for man in managers:
            if man.email== mail and man.password == mdp:
                return redirect('http://127.0.0.1:8000/biblio/'+str(man.id))
        else:
                messages.success(request,' Email or Password is incorrect!')
                return render(request, 'bib/login.html' )    
 else:
    return render(request, 'bib/login.html')

def logout(request):
    return render(request, 'bib/mainmenu.html')


@csrf_exempt
def lend(request,man_id):
    manager = get_object_or_404(Manager,id=man_id)
    if request.method== "POST":
        data =request.POST
        liv_id=data.get('livs').split('+')[0]
        livre = get_object_or_404(Livre,id=liv_id)
        adherent = get_object_or_404(Adherent,id=data.get('mems'))
        instance = empreinte()
        instance.liv_id = livre
        instance.man_id = manager
        instance.ad_id = adherent
        instance.end = data.get('dt')
        livre.qt-= 1
        livre.save()
        instance.save()
    livres=Livre.objects.all()
    adherents=Adherent.objects.all()
    return render(request, 'bib/lend.html',context={"manager":manager,"livres":livres,"adherents":adherents})


@csrf_exempt
def sell(request,man_id):
    manager = get_object_or_404(Manager,id=man_id)
    if request.method== "POST":
        data =request.POST
        liv_id=data.get('livs').split('+')[0]
        livre = get_object_or_404(Livre,id=liv_id)
        adherent = get_object_or_404(Adherent,id=data.get('mems'))
        instance = transaction()
        instance.liv_id = livre
        instance.man_id = manager
        instance.ad_id = adherent
        instance.montant = data.get('montant')
        instance.qt = data.get('qtin')
        instance.confirmed = True
        livre.qt-= int(instance.qt)
        livre.save()
        instance.save()
    livres=Livre.objects.all()
    adherents=Adherent.objects.all()
    return render(request, 'bib/sell.html',context={"manager":manager,"livres":livres,"adherents":adherents})


@csrf_exempt
def viewlends(request,man_id):
    manager = get_object_or_404(Manager,id=man_id)
    if request.method== "POST":
        data =request.POST
        emp = get_object_or_404(empreinte,id=data.get('cheezy'))
        livre = get_object_or_404(Livre,nom=emp.liv_id)
        emp.end= datetime.datetime.now()  
        emp.returned = True
        livre.qt +=1
        livre.save()
        emp.save()
    empreintesfalse=empreinte.objects.all().filter(returned=False,man_id=man_id)
    empreintestrue=empreinte.objects.all().filter(returned=True,man_id=man_id)
    return render(request, 'bib/viewlends.html',context={"manager":manager,"empreintesfalse":empreintesfalse,"empreintestrue":empreintestrue})


@csrf_exempt
def viewsales(request,man_id):
    manager = get_object_or_404(Manager,id=man_id)
    if request.method== "POST":
        data =request.POST
        tran = get_object_or_404(transaction,id=data.get('cheezy'))
        livre = get_object_or_404(Livre,nom=tran.liv_id)
        livre.qt += tran.qt
        livre.save()
        tran.delete()
    sales=transaction.objects.all().filter(man_id=man_id,confirmed=True)
    return render(request, 'bib/viewsales.html',context={"manager":manager,"sales":sales})

@csrf_exempt
def regcus(request,man_id):
    manager = get_object_or_404(Manager,id=man_id)
    if request.method== "POST":
        data =request.POST
        clients=Adherent.objects.all()
        nom=data.get('name')
        prenom=data.get('fam')
        mail = data.get('email')
        mdp = data.get('password')
        mdpcon = data.get('passcon')
        for clt in clients:
            print(clt.email)
            if clt.email== mail:
                messages.success(request,' This Email already exists!')
                return render(request, 'bib/regcus.html',{"manager":manager} ) 
            else:
                if mdp == mdpcon:
                    instance = Adherent()
                    instance.nom = nom
                    instance.prenom = prenom
                    instance.email = mail
                    instance.password = mdp
                    instance.save()
                    return render(request, 'bib/regcus.html',{"manager":manager} )
                else:
                    messages.success(request,' Passwords do not match!')
                    return render(request, 'bib/regcus.html',{"manager":manager} )
    else:
        return render(request,"bib/regcus.html",{"manager":manager})
    
    
@csrf_exempt
def cuslogin(request):
 if request.method== "POST":
        data =request.POST
        clients=Adherent.objects.all()
        mail = data.get('email')
        mdp = data.get('password')
        for clt in clients:
            if clt.email== mail and clt.password == mdp:
                return redirect('http://127.0.0.1:8000/biblio/clt'+str(clt.id))
        else:
                messages.success(request,' Email or Password is incorrect!')
                return render(request, 'bib/cuslogin.html' )    
 else:
    return render(request, 'bib/cuslogin.html')


@csrf_exempt
def signup(request):
    if request.method== "POST":
        data =request.POST
        clients=Adherent.objects.all()
        nom=data.get('name')
        prenom=data.get('fam')
        mail = data.get('email')
        mdp = data.get('password')
        mdpcon = data.get('passcon')
        for clt in clients:
            print(clt.email)
            if clt.email== mail:
                messages.success(request,' This Email already exists!')
                return render(request, 'bib/signup.html') 
            else:
                if mdp == mdpcon:
                    instance = Adherent()
                    instance.nom = nom
                    instance.prenom = prenom
                    instance.email = mail
                    instance.password = mdp
                    instance.save()
                    return render(request, 'bib/signup.html' )
                else:
                    messages.success(request,' Passwords do not match!')
                    return render(request, 'bib/signup.html' )
    else:
        return render(request,'bib/signup.html')
    

@csrf_exempt
def hello(request):
    return render(request,"bib/mainmenu.html")

    
@csrf_exempt
def loca(request):
    return render(request,"bib/location.html")


@csrf_exempt
def contact(request):
    return render(request,"bib/contact.html")


@csrf_exempt
def faq(request):
    return render(request,"bib/faq.html")


@csrf_exempt
def clthome(request,clt_id):
 client = get_object_or_404(Adherent,id=clt_id)  
 if request.method== "POST":
    data =request.POST
    nom = data.get('nom')
    prenom = data.get('prenom')
    mail = data.get('mail')
    password = data.get('password')
    client.nom = nom
    client.prenom = prenom
    client.email = mail
    client.password = password
    client.save()
 return render(request,"bib/clthome.html",{"client":client})


@csrf_exempt
def buy(request,clt_id):
 client = get_object_or_404(Adherent,id=clt_id)  
 if request.method== "POST":
    data =request.POST
    liv_id = data.get('idliv')
    livre = get_object_or_404(Livre,id=liv_id)
    instance = transaction()
    instance.liv_id = livre
    items = list(Manager.objects.all())
    random_mans = random.sample(items, 2)
    manager= random.choice(random_mans)
    instance.man_id = manager
    instance.ad_id = client
    instance.montant = data.get('montant')
    instance.qt = data.get('qtsale')
    instance.confirmed = False
    livre.qt-= int(instance.qt)
    livre.save()
    instance.save()
 livres=Livre.objects.filter(qt__gt=0)
 return render(request,"bib/buy.html",context={"client":client,"livres":livres})


@csrf_exempt
def contactlog(request,clt_id):
    client = get_object_or_404(Adherent,id=clt_id)  
    return render(request,"bib/contactlog.html",{"client":client})


@csrf_exempt
def faqlog(request,clt_id):
    client = get_object_or_404(Adherent,id=clt_id)  
    return render(request,"bib/faqlog.html",{"client":client})


@csrf_exempt
def localog(request,clt_id):
    client = get_object_or_404(Adherent,id=clt_id)  
    return render(request,"bib/locationlog.html",{"client":client})


@csrf_exempt
def cart(request,clt_id):
    client = get_object_or_404(Adherent,id=clt_id) 
    if request.method== "POST":
        data =request.POST
        tran = get_object_or_404(transaction,id=data.get('idsale'))
        livre = get_object_or_404(Livre,nom=tran.liv_id)
        livre.qt += tran.qt
        livre.save()
        tran.delete()
    sales=transaction.objects.all().filter(ad_id=clt_id,confirmed=False)
    livres=Livre.objects.all()
    return render(request,"bib/cart.html",context={"client":client,"sales":sales,"livres":livres})


@csrf_exempt
def pay(request,clt_id,sale_id):
    client = get_object_or_404(Adherent,id=clt_id)
    sale = get_object_or_404(transaction,id=sale_id)
    newprice = sale.montant + 15
    if request.method== "POST":
        sale.montant = newprice
        sale.confirmed = True
        print("bruh")
        sale.save()
        return render(request,"bib/thanks.html")
    return render(request,"bib/pay.html",context={"client":client,"sale":sale,"newprice":newprice})