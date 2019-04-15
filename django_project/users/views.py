from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, TemplateView,CreateView,DeleteView,DetailView
from users.models import Permitidos
from django.contrib.auth.models import User
from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        email=(request.POST)['email']
        
        if form.is_valid():
            emails=Permitidos.objects.all()
            #print(emails)
            emails_permitidos=[e.email for e in emails]
            if email not in emails_permitidos:
                return HttpResponse('<h2>Email não permitido. Entre em contato com o administrador.<h2>')
            part=User.objects.all()
            participantes=[p.email for p in part]
            #print(participantes)
            #if form.is_valid() == False:
                #return HttpResponse('<h2>Email ja em uso. Entre em contato com o administrador 1.<h2>')
            if  email not in participantes:
                print('part',participantes)
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Sua conta foi criada com sucesso')
                return redirect('login')
            else:
                messages.warning(request, f'Email já em uso!')
                #return HttpResponse('<h2>Email ja em uso. Entre em contato com o administrador 2.<h2>')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Sua conta foi atualizada!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


