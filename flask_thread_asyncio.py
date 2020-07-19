from flask import Flask
import threading, asyncio, sys, time
from random import randint

app = Flask(__name__)

"""
#Usar a opcao abaixo, quando NAO estiver setado as variaveis dentro da thread como esta sendo feito na def main() setando host e port direto na thread
app.config.update (
    DEBUG=True,
    SERVER_NAME = 'localhost:8000',
    SECRET_KEY='secret!'
    ...
)
"""

#Criacao da rota padrao em flask.
@app.route("/")
def main():
    return "Hello World!"

#Funcao rodando em modo Assincrono. Nao usar time.sleep() e sim a funcao sleep() do proprio asyncio conforme abaixo
async def contador1():
    while True:
        print(f'Contador1: {randint(0,9)}')
        #No comando abaixo que da uma pausa de 1 segundo, ele da instrucao pro sistema nao esperar e ja chamar o que ele tiver que chamar, que nesse caso
        #e a funcao contador2(), ou seja ja estou avisando que nao quero que me espere pois pode demorar.
        await asyncio.sleep(1)

#Funcao rodando em modo Assincrono. Nao usar time.sleep() e sim a funcao sleep() do proprio asyncio conforme abaixo
async def contador2():
    while True:
        print(f'Contador2: {randint(0,9)}')
        #No comando abaixo que da uma pausa de 1 segundo, ele da instrucao pro sistema nao esperar e ja chamar o que ele tiver que chamar, que nesse caso
        #e a funcao contador1(), ou seja ja estou avisando que nao quero que me espere pois pode demorar.
        await asyncio.sleep(2)

#Funcao rodando em modo Sincrono. Nesse caso e usado o time.sleep() que é bloqueante.
#Nesse caso da funcao sincrona, se usar o While True como nas assincronas e rodar um loop infinito, as outras funcoes nao serao chamadas, 
#pois como ela e sincrona, o python ficara esperando ela terminar para chamar as outras da sequencia.. contador1() e contador2(), que sao as proximas nas chamadas
#dentro da funcao main() , nesse caso usei um loop de 10 passos, ou seja o contador1() e contador2() terao que esperar essa funcao completar os 10 loops do
#passo para serem chamadas. 
def contador10():
    for i in range(0,10):
        print(f'Contador10: {i}')
        time.sleep(1)

def main():
    #Rodando uma thread separada para o Flask. O unico jeito de cionseguir rodar sem bloqueio o flask, foi usando direto app.run dentro do target da thread sem os ()
    #normamente usa-se o app.run(), tive que fazer app.run e passar os parametros do flask via app.config.update, para o flask deixar passar as proximas functions!
    threading.Thread(target=app.run, daemon=True, kwargs={'host':'0.0.0.0', 'port':5123}).start()
    
    #Chama a funcao Sincrona, contador10(), como ela e sincrona o sistema vai ter que esperar para comecar as proximas funcoes abaixo: contador1() e contador2()
    contador10()

    #O modelo abaixo serve para executar funcoes em modo assincrono, onde uma nao fica esperando a outra, elas ficam executando todas conforme finalizar 
    #mostram os resultados. No caso de rodar um While True vao ficar para sempre juntas executando, sem uma esperar a outra como o caso da contador10() que e sincrona.
    loop = asyncio.get_event_loop()
    #Nesse caso vamos rodar em modo assincrono as funcoes contador1() e contador2() usando a lib asyncio do Python3.7
    tasks = [loop.create_task(contador1()), loop.create_task(contador2())]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Finalizando...")
        sys.exit()
    except Exception as e:
        print(f"Erro: {e}")