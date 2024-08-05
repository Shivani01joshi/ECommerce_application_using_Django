from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . forms import LoginForm, MyPasswordResetForm,MyPasswordChangeForm,MysetPasswordForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('category-title/<str:val>/', views.CategoryTitle.as_view(), name='category-title'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('addtocart/<int:product_id>/', views.addtocart, name='addtocart'),
    path('cart/', views.show_cart, name='showcart'),
    
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('plus_cart/', views.plus_cart),
    path('remove_cart/', views.remove_cart),
    path('updateAddress/<int:pk>/', views.updateAddress.as_view(), name='updateAddress'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordChange/', auth_views.PasswordChangeView.as_view(
        template_name='app/PasswordChange.html',
        form_class=MyPasswordChangeForm,
        success_url='/passwordChange/done/'
    ), name='passwordChange'),
    path('passwordChange/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/PasswordChangeDone.html'
    ), name='passwordChangeDone'),
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MysetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('product/<int:product_id>/', views.addtocart, name='addtocart'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
