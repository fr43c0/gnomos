from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import Post,Document,Avisos
from users.models import Permitidos
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
import bs4 as bs
import requests
from django.http import HttpResponse
import json
from django.core.paginator import Paginator


class DocDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    success_url = '/'

    def test_func(self):
        doc = self.get_object()
        if self.request.user ==doc.author:
            return True
        return False

class DocDetailView(LoginRequiredMixin,DetailView):
    model = Document  

class DocsView(LoginRequiredMixin,ListView):
    model = Document
    template_name = 'blog/arquivos.html' 
    context_object_name = 'arquivos'
    ordering = ['-autor']
    paginate_by = 20
    
    # def post(self, request, *args, **kwargs):
    #     self.status_form = StatusForm(self.request.POST or None)
    #     if self.status_form.is_valid():
    #         print('qqqqqqqqqqqqq',self.status_form)
   

# def upLoadPostFiles(request):
#     model=Post
#     form=PostForm()
#     fields = ['title', 'content','embedded','file']
#     if request.method=='POST':
#         form=PostForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.savs=soup.find('script',{'type':"application/ld+json"})e()
#             return rs=soup.find('script',{'type':"application/ld+json"})ender(request, 'blog/home.html')
#     else:s=soup.find('script',{'type':"application/ld+json"})
#         form=PostFors=soup.find('script',{'type':"application/ld+json"})m()
#     return render(request,'blog/upload.html',{'form':form})
        #uploaded_file=request.FILES['document']
        #print(uploaded_file.name,uploaded_file.size)
        #fs = FileSystemStorage()
        #filename = fs.save(uploaded_file.name, uploaded_file)
        #uploaded_file_url = fs.url(filename)
        #print('uploaded_file_url',uploaded_file_url)
    
# def avisos(request):
#     return render(request,'blog/avisos.html')

 ###   
class AvisosListView(LoginRequiredMixin,ListView):
    model = Avisos
    template_name = 'blog/avisos.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'avisos'
    ordering = ['-date_posted']

class AvisosDetailView(LoginRequiredMixin,DetailView):
    model = Avisos   


class AvisosCreateView(LoginRequiredMixin, CreateView):
    model = Avisos
    fields = ['title', 'content','imagem','link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AvisosUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Avisos
    fields = ['title', 'content','imagem','link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        aviso = self.get_object()
        if self.request.user == aviso.author:
            return True
        return False


class AvisosDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Avisos
    success_url = '/'

    def test_func(self):
        aviso = self.get_object()
        if self.request.user == aviso.author:
            return True
        return False

###
class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class VideosListView(ListView):
    model = Post
    template_name = 'blog/h_videos.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 25



class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content','imagem','embedded','link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content','imagem','embedded','link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ParticipantesTemplateView(LoginRequiredMixin,TemplateView):
    part2=[]
    model=User
    template_name='users/participantes.html'
    part=User.objects.all()
    participantes=[p.username for p in part]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participantes"] = User.objects.all()
        return context
    
class EmailCreateView(LoginRequiredMixin,CreateView):
    fields=('email',)
    model=Permitidos
    #success_url = 'users:detalhe'
    #template_name='accounts/super'
    
class EmailListView(LoginRequiredMixin,ListView):
    model=Permitidos
    context_object_name = 'permitidos'
    template_name='users/permitidos/'

class EmailDetailView(LoginRequiredMixin,DetailView):
    model=Permitidos
    context_object_name = 'permitido'
   

class EmailDeleteView(LoginRequiredMixin,DeleteView):
    model=Permitidos
    success_url =reverse_lazy('permitidos')

def abrir_pagina(url):
    context={}
    headers={}
    headers['User-Agent']='Mozila/5.0 (X11; Linux i686)'
    pagina=requests.get(url,headers=headers)
    conteudo=pagina.content
    soup=bs.BeautifulSoup(conteudo,'lxml')
    #[s.extract() for s in soup('p')]###
    titulo=soup.find('meta',{'property':'og:title'})['content']
    descricao=soup.find('meta',{'property':'og:description'})['content']
    img=soup.find('meta',{'property':'og:image'})['content']
    link=soup.find('meta',{'property':'og:url'})['content']
    context['t']=titulo
    context['l']=link
    context['d']=descricao
    context['i']=img
    return context
def thumb(request):
    context={}
    return render(request, 'blog/testeLink.html' )

def abrePag(request):
    if request.method=='POST':
        r=request.POST
        url=(r['url'])
        #print(url)
        #context={'b':abrir_pagina(url)}
        #print(type(context['b']))
        #return render(request,'lerjor/red.html',context)
        #return HttpResponse(abrir_pagina(url))
        context=abrir_pagina(url)

        return  render (request,'blog/testeLink.html',context)
    else:
        return render(request,'blog/pag.html')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def home(request):

    context = {'posts': Post.objects.all().order_by('-date_posted')    }
    paginate_by = 5
    return render(request, 'blog/home.html', context)

def videos(request):
    context = {'posts': Post.objects.all().order_by('-date_posted')    }
    #posts=[{i:context[i]} for i in context.keys()]
    paginator = Paginator(context,2)
    return render(request, 'blog/h_videos.html',context)

    
def imagens(request):

    context = {'posts': Post.objects.all().order_by('-date_posted')    }
    paginate_by = 5
    return render(request, 'imagens.html', context)

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/arquivos')
    else:
        form = DocumentForm()
    return render(request, 'blog/upload.html', {
        'form': form
    })