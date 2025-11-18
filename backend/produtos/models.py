from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    arquivo = models.FileField(upload_to="matrizes/")

class categoria(models.Model):
    Categoria = models.ForeignKey(Produto, on_delete=models.CASCADE)