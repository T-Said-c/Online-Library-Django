from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('manager_login',views.login,name="login"),
    path("<int:man_id>", views.home,name="home"),
    path('',views.logout,name="logout"),
    path("<int:man_id>/lend",views.lend,name="lend"),
    path("<int:man_id>/sell",views.sell,name="sell"),
    path("<int:man_id>/view_lends",views.viewlends,name="view_lends"),
    path("<int:man_id>/view_sales",views.viewsales,name="view_sales"),
    path("<int:man_id>/register_customer",views.regcus,name="register_customer"),
    path("customer_login",views.cuslogin,name="customer_login"),
    path("customer_signup",views.signup,name="customer_signup"),
    path("location",views.loca,name="location"),
    path("contact_us",views.contact,name="contact_us"),
    path("FAQ",views.faq,name="FAQ"),
    path("clt<int:clt_id>", views.clthome,name="clthome"),
    path("clt<int:clt_id>/shop", views.buy,name="shop"),
    path("clt<int:clt_id>/contact_us",views.contactlog,name="contact_us"),
    path("clt<int:clt_id>/location",views.localog,name="location"),
    path("clt<int:clt_id>/FAQ",views.faqlog,name="FAQ"),
    path("clt<int:clt_id>/cart",views.cart,name="cart"),
    path("clt<int:clt_id>/sale<int:sale_id>/pay",views.pay,name="pay"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
