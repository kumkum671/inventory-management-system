from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from . utils import generate_password
from . forms import CustomAuthenticationForm, UserRegisterForm
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth import login
from django.shortcuts import redirect
from . models import User
from lab.mixins import RedirectLoggedInUserMixin, AdminOnlyAccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class LandingPageView(RedirectLoggedInUserMixin, generic.TemplateView):
    template_name = 'landing_page.html'


class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = 'core/register-user.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_admin = True
        user.save()
        return super(UserRegisterView, self).form_valid(form)  
    
    def get_success_url(self):
        return reverse('core:login')  


class LoginView(RedirectLoggedInUserMixin, views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'core/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('landing-page')
    
    
class LogoutView(views.LogoutView):
    template_name = 'core/logout.html'


class ChangePasswordView(LoginRequiredMixin, views.PasswordChangeView):
    template_name = 'core/change-password.html'
    success_url = reverse_lazy('landing-page')


class ResetPasswordView(RedirectLoggedInUserMixin, views.PasswordResetView):
    email_template_name = 'core/password_reset/password_reset_email.html'
    html_email_template_name = 'core/password_reset/password_reset_email.html'
    subject_template_name = 'core/password_reset/password_reset_subject.txt'
    success_url = reverse_lazy('core:done-password-reset')
    template_name = 'core/password_reset/password_reset_form.html'


class DonePasswordResetView(RedirectLoggedInUserMixin, views.PasswordResetDoneView):
    template_name = 'core/password_reset/password_reset_done.html'


class ConfirmPasswordResetView(RedirectLoggedInUserMixin, views.PasswordResetConfirmView):
    success_url = reverse_lazy('core:complete-password-reset')
    template_name = 'core/password_reset/password_reset_confirm.html'


class CompletePasswordResetView(RedirectLoggedInUserMixin, views.PasswordResetCompleteView):
    template_name = 'core/password_reset/password_reset_complete.html'


class AddUserView(LoginRequiredMixin, AdminOnlyAccessMixin, generic.CreateView):
    fields = ['email', 'first_name', 'last_name']
    model = User
    template_name = 'core/add-user-form.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = str(generate_password())
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        
        user = User.objects.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        return redirect('lab:lab-list')
        
