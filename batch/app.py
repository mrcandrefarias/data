import loadEventos
from time import sleep

if __name__ == '__main__':
    # aguarda 30 segundos, para garantir que container do banco de 
    # dados ja foi iniciado
    sleep(30)
    loadEventos.buscarEventos()
    loadEventos.carregarDetalhesEventos()
