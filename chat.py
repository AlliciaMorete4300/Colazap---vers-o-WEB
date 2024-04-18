from usuario import Usuario
from conexao import Conexao
from mensagem import Mensagem
from contato import Contato
class Chat:

    def __init__(self, nome_usuario:str, telefone_usuario:str):
        
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario

    def enviar_mensagem(self,conteudo:str,destinatario:Contato) -> bool:
      mydb = Conexao.conectar()

      # self.conteudo = conteudo 
      # tel_remetente = self.usuario.telefone
      # tel_destinatario = self.contato_escolhido
      # mensagem = conteudo
      # mydb.commit()

    
        
      mycursor = mydb.cursor()
      sql = "INSERT INTO tb_mensagem (tel_remetente, mensagem , tel_destinatario) VALUES (%s,%s,%s)" #s = string

      val = (self.telefone_usuario, conteudo, destinatario.telefone )
      mycursor.execute(sql, val)
      mydb.commit()
      return True
    
    

    
    def verificar_mensagem(self,quantidade:int, destinatario:Contato) :
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()
        sql = f"SELECT t.nome, m.mensagem FROM tb_usuario t INNER JOIN tb_mensagem m ON m.tel_remetente = t.tel WHERE m.tel_remetente = '{self.telefone_usuario}' AND m.tel_destinatario = '{destinatario.telefone}' OR tel_remetente ='{destinatario.telefone}' AND tel_destinatario = '{self.telefone_usuario}' ORDER BY m.id_mensagem" 

        mycursor.execute(sql)
        resultado = mycursor.fetchall()

        lista_mensagens =[]
        for linha in resultado:
            mensagem = {"nome":linha[0], "mensagem":linha[1]}
            lista_mensagens.append(mensagem)
      
      


        return (lista_mensagens)

    def retornar_contatos(self):
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()
        sql = "SELECT nome, tel FROM tb_usuario ORDER BY nome " 

        mycursor.execute(sql)
        resultado = mycursor.fetchall()

        lista_contatos =[]

        lista_contatos.append({"nome":"TODOS","telefone":""})

        for linha in resultado:
          contato = {"nome":linha[0],"telefone":linha[1]}
          lista_contatos.append(contato)
        mydb.commit()

  

        return(lista_contatos)
    
    
