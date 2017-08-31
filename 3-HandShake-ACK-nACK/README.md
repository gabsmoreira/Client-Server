# Camada Física - Projeto 1 - COM-Client-Server
Gabriel Moreira e Daniel Ruhman


## Diagrama de camadas

 ![Diagrama de camadas](images/final.001.jpeg)


## Diagrama de funcionamento

 ![Diagrama de funcionamento](images/final.002.jpeg)



## Datagrama Proj 2

 ![Datagrama](images/datagrama.png)

## Documentação projeto 3:

Nesse projeto, foi implementado um protocolo de handshake na camada de enlace.
Esse protocolo garante ao Client que seus dados só serão enviados quando o Server estiver
pronto para recebe-los.
Além disso, foi implementado também um protocolo de reconhecimento via ACK e nACK de maneira que o client sempre
 sabe o status dos dados e, caso necessario, pode reenviar o pacote.

 Para formar a conexão com o Server, o Client envia um pacote SYN para o Server, que deve responder se ele recebeu esse SYN. Se receber, ele envia um pacote comando ACK, reconhecendo que recebeu o SYN e em seguida envia um SYN para confirmar a conexão. O Client recebe esses pacotes ACK + SYN, e  então responde ACK para confirmar a conexão também. Com a conexão estabelecida, o Client pode começas a enviar os dados normalmente. Se em algum momento um nAck for enviado por alguma das partes, o handshake reinicia. A figura a seguir ilustra esse Handshake, de maneira que a "menina" é o Client e o HD, o Server (a conexão é estabelecida quando ele fica com o check verde):

![Datagrama](images/Handshake.png)