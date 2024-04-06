import datetime
from django.db import models
from django.utils import timezone

class Pergunta(models.Model): #definida com 2 atributos
    texto = models.CharField(max_length=150) #parametro
    pub_date = models.DateTimeField('Data de publicação')
    def __str__(self): #definir método str  todo método em python precisa receber um argumento self- referencia para o próprio objeto
        return '{} ({})'.format(self.texto, self.id)
    def publicada_recentemente(self):
        agora = timezone.now()
        return self.pub_date >= agora - datetime.timedelta(hours=24)

class Alternativa(models.Model): #definida com 3 atributos
    texto = models.CharField(max_length=100)#parametro)
    quant_votos = models.IntegerField('Quantidade de votos', default=0)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE) #pergunta ao qual esta associada - atributo de relacionamento - relaciona um objeto'alternativa' ao objeto 'pergunta'
    def __str__(self):
        return '{} ({})'.format(self.texto, self.id)


# Toda classe de modelo precisa herdar de uma superclasse chamada model, pq toda classe de modelo é um model..
#Necessário definir os atributos por causa do mecanismo de mapeamento ao objeto relacional = mapear todas as definições de classe de modelo para o banco de dados relacional
#cada classe de modelo se transformará em uma tabela de dados
#cada atributo se transformará em uma coluna de dados (para isso funcionar precisa indicar quais os tipos associados a esses atributos)
