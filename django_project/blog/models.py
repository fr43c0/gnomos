from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#from embed_video.fields import EmbedVideoField
import requests
from bs4 import BeautifulSoup as BS
from time import sleep
class Post(models.Model):
    title = models.CharField('Título  (o titulo do seu post servirá como link para editá-lo posteriormente)',max_length=100,default='post sem título')
    content = models.TextField('Conteúdo',default='-')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    embedded=models.CharField('Cole aqui o Link de videos (Youtube & Vimeo)',max_length=250,blank=True, null=True)
    link=models.URLField('Cole aqui o Link de outras paginas', max_length=250,blank=True, null=True)
    imagem=models.ImageField(upload_to='blog_images', blank=True, null=True)
    titulo_og=models.CharField(max_length=250,blank=True, null=True)
    descricao_og=models.CharField(max_length=250,blank=True, null=True)
    img_og =models.CharField(max_length=250,blank=True, null=True)
    origem_og=models.CharField(max_length=250,blank=True, null=True)
    link_og=models.URLField( max_length=250,blank=True, null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
  
    def e_status(self):
        if str(self.embedded ) not in ('',"None"):

            if 'watch?' in str(self.embedded):
                e_status=True
                url_fim=self.embedded.split('/')[-1]
                url_fim2=url_fim.split('=')[-1]
                url_fim3='embed/'+url_fim2
                url=self.embedded.replace(url_fim,url_fim3)
                return {'url':url}
            elif 'vimeo' in str(self.embedded):
                e_status=True
                url_fim=self.embedded.split('/')[-1]
                url_fim2=url_fim.split('=')[-1]
                url='https://player.vimeo.com/video/'+url_fim2
                
                return {'url':url}
            else:
                return self.embedded
                
        else:
            e_status=False
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)   
    #def getLink(self):
        if str(self.link) not in ('',"None") and str(self.link_og)=='None':
                print(self.link_og)
                print('verificou que link nao e vazio')
            #if self.img_og  in ('',"None") or self.link_og  in ('',"None"):
                url=self.link
                context={}
                headers={}
                headers['User-Agent']='Mozila/5.0 (X11; Linux i686)'
                pagina=requests.get(url,headers=headers)
                conteudo=pagina.content
                soup=BS(conteudo,'lxml')
                #s=soup('script')
                [s.extract() for s in soup('script')]
                [s.extract() for s in soup('p')]###
                m=soup('meta')
                try:
                    titulo=soup.find('meta',{'property':'og:title'})['content']
                except:
                    titulo='Titulo nao encontrado'
                try:
                    descricao=soup.find('meta',{'property':'og:description'})['content']
                except:
                    descricao='link'
                img=soup.find('meta',{'property':'og:image'})['content']
                try:
                    origem=soup.find('meta',{'property':'og:site_name'})['content']
                except:
                    origem=soup.find('meta',{'property':'og:url'})['content'].split('/')[2].capitalize()
                linkog=soup.find('meta',{'property':'og:url'})['content']
                # context['t']=titulo
                # context['l']=linkog
                # context['d']=descricao
                # context['i']=img
                # context['o']=origem
                if self.content=='-':
                    self.content=' '
                self.link_og=linkog
                self.origem_og=origem
                self.titulo_og=titulo
                self.img_og=img
                self.descricao_og=descricao
                self.save()
                sleep(5)
                #return context    
            #else:
                #getLink=False
                
        else:
            pass  


class Document(models.Model):
    description = models.CharField('Título',max_length=255, blank=True)
    titulo = models.CharField('Título',max_length=255, blank=True)
    autor= models.CharField('Autor', max_length=255,blank=True, null=True)
    document = models.FileField('Arquivo',upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    capa=models.ImageField(upload_to='arquivos',blank=True, null=True)
    
    
    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('doc-detail', kwargs={'pk': self.pk})

class Avisos (models.Model):
    title = models.CharField('Título',max_length=255,)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('Conteúdo')
    date_posted = models.DateTimeField(default=timezone.now)
    link=models.URLField('Cole aqui o Link para outras paginas', max_length=250,blank=True, null=True)
    imagem=models.ImageField(upload_to='avisos_images', blank=True, null=True)
    

    class Meta:
        
        verbose_name_plural = 'Avisos'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('avisos-detail', kwargs={'pk': self.pk})