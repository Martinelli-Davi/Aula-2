from django.db import models
import os
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    estoque = models.IntegerField(default=0)
    foto = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return self.nome
    
    @classmethod
    def criar_produto(cls, nome, estoque, foto):
        produto = cls(nome=nome, estoque=estoque, foto=foto)
        produto.save()
        return produto
    
    @classmethod
    def vender_produto(cls, produto_id, quantidade):
        try:
            produto = cls.objects.get(id=produto_id)
            if produto.estoque >= quantidade:
                produto.estoque -= quantidade
                produto.save()
                return True
            else:
                return False
        except cls.DoesNotExist:
            return False
        
@receiver(pre_save, sender=Produto)
def ajustar_foto_produto(sender, instance, **kwargs):
    if instance.foto:
        instance.foto.name = f"{os.path.basename(instance.foto.name)}"

def pre_delete_foto(sender, instance, **kwargs):
    if instance.foto:
        foto_path = os.path.join(settings.MEDIA_ROOT, instance.foto.name)
        if os.path.exists(foto_path):
            os.remove(foto_path)