from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('user-login/',views.login_page,name="user-login"),
    path('user-logout/',views.logout_page,name="user-logout"),
    path("register",views.register,name="register"),
    path("",views.home_page,name="home"),
    path("room/<str:pk>",views.room,name="room"),
    path("create-room/",views.create_room,name="create_room"),
    path('update-room/<str:pk>',views.update_room,name="update_room"),
    path('delete-room/<str:pk>',views.delete_room,name="delete_room"),
    path('delete-message/<room_id>/<message_id>/',views.delete_message,name="delete-message"),
    path('profile/<id>/',views.profile,name="profile"),
    path('update_user/',views.update_user,name="update_user"),
    path('topics/',views.all_topics,name="all_topics"),
    path('recents/',views.recents,name="recents"),

]

urlpatterns +=  static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)