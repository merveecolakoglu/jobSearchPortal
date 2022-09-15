from django.urls import path

from users import views

app_name='users'

urlpatterns = [
    path('home/',views.homeView,name='home'),

    path('employer-register/',views.registerEmployerView,name='employer-register'),

    path('account/',views.userAccount,name='account'),
    path('edit-account/',views.editAccount,name='edit-account'),

    path('profile/<str:pk>/',views.userProfile,name='user-profile'),

    path('create-skill/',views.createSkill,name='create-skill'),
    path('update-skill/<str:pk>/',views.updateSkill,name='update-skill'),
    path('delete-skill/<str:pk>/',views.deleteSkill,name='delete-skill'),

    path('inbox/',views.inbox,name='inbox'),
    path('message/<str:pk>/',views.viewMessage,name='message'),
    path('create-message/<str:pk>/',views.createMessage,name='create-message'),
]