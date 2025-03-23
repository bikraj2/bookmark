from django.urls import include, path
from .views import dashboard, edit, register, user_detail, user_follow  ,user_list
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('login/',auth_views.LoginView.as_view(),name="login"),
    # path('logout/',auth_views.LogoutView.as_view(),name="logout"),
    # path('password-change/',view=auth_views.PasswordChangeView.as_view(),name="password_change"),
    # path('password-change/done/',view=auth_views.PasswordChangeDoneView.as_view(),name="password_change_done"),
    # path('password-resset/',view=auth_views.PasswordResetView.as_view(),name="password_reset"),
    # path('password-reset/done/',view=auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    # path('password-reset/<uidb64>/<token>/',view=auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    # path('password-reset/complete/',view=auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    #
    path('',include('django.contrib.auth.urls')),
    path('register/',register,name="register"),
    path('edit/',edit,name="edit"),
    path('users/',user_list,name="user_list"),
    path('users/follow/',user_follow,name="user_follow"),
    path('users/<username>/',user_detail,name="user_detail"),
    path('dashboard/',view=dashboard,name="dashboard")
] 

if settings.DEBUG:
    urlpatterns+= static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
