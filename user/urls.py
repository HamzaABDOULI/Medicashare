from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name='user'
urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('',views.home,name="profile"),
    path('historics/',views.historique,name="historics"),
    path('saveToHistorics/<int:id>/',views.saveToHistorics,name="saveToHistorics"),####
    
    path('add-new-request/',views.newRequest,name="newRequest"),
    path('add-new-donation/',views.newDonation,name="newDonation"),
    path('delete-post/<int:post_id>/',views.delete_post,name="delete_post"),
    path('update-post/<int:post_id>/',views.update_post,name="update_post"),
    path('notifications/',views.notifications,name="notification"),
    path('detail/<str:slug_title>-id=<int:post_id>/',views.post_detail,name="detail"),
    path('notifications/detail/<int:notif_id>/',views.notif_detail,name="notif_detail"),
    path('my-posts/',views.privatePosts,name="privatePosts"),
    path('update-profile/<str:username>/',views.update_profile,name="update_profile"),####
    path('search-<str:choice>/<str:title>',views.search,name='search'),
    path('search-<str:choice>/<str:title>/<str:c_place>',views.search,name='search'),
    
    path('update_notifications_number/',views.nots,name="nots"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)