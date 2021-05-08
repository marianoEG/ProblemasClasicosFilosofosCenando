import threading
import time
import random
import logging


class Filosofo(threading.Thread):

    sentados = threading.Semaphore(4)

    def __init__(self, izqTenedor, derTenedor, nombre):
        super().__init__()
        self.izqTenedor = izqTenedor
        self.derTenedor = derTenedor
        self.name = nombre
        print(f'Filósofo {self.name} se sentó en la mesa')

    def run(self):
        print(f'Filósofo {self.name} comenzó a Pensar')
        while True:
            time.sleep(random.randint(1,5))
            print(f'Filósofo {self.name} terminó de pensar {threading.current_thread()}')
            self.sentados.acquire()
            try:
                self.izqTenedor.acquire()
                time.sleep(random.randint(1,5))
                try:
                    print(f'Filósofo {self.name} obtuvo el tenedor Izquierdo {threading.current_thread()}')
                    self.derTenedor.acquire()
                    try:
                        print(f'Filósofo {self.name} los dos tenedores y esta comiendo {threading.current_thread()}')
                    finally:
                        self.derTenedor.release()
                        print(f'Filósofo {self.name} liberó el tenedor Derecho {threading.current_thread()}')
                finally:
                    self.izqTenedor.release()
                    print(f'Filósofo {self.name} liberó el tenedor Izquierdo {threading.current_thread()}')
            finally:
                self.sentados.release()


def main():
    # filosofos = []
    threads = []
    tenedor = [threading.RLock() for i in range(5)]
    nombres = ["Socrates", "Platón", "Aristóteles", "Locke", "Descartes"]

    for i in range(5):
        time.sleep(random.randint(1,2))
        filosofo = Filosofo(tenedor[i], tenedor[(i+1) % 5], nombres[i])
        threads.append(filosofo)
        filosofo.start()

    for i in threads:
        i.join()

if __name__=='__main__':
    main()


