""" The room party problem

Problema de sincronización obtenido de: The Little Book of Semaphores. Allen B Downey
Autor: Santos Gallegos
"""

import threading
import time


class Decano:
    def __init__(self):
        self.dentro = False

    def __entrar(self):
        print("Decano entrando")
        self.dentro = True

    def interrumpir_fiesta(self):
        self.__entrar()
        print("La fiesta termino. Todos fuera!")

    def iniciar_busqueda(self):
        self.__entrar()
        print("Buscando...")

    def salir(self):
        self.dentro = False
        print("Decano fuera")

    def esperar(self):
        self.dentro = False
        print("Esperando...")


class Estudiante:
    estudiantesin = 0  # Númeoro de estudiantes que está dentro del cuarto

    def __init__(self):
        pass

    def entrar(self):
        print("Estudiante entrando")
        Estudiante.estudiantesin += 1

    def fiesta(self):
        print("Fiesta!")
        time.sleep(0.2)  # Sólo para simular el tiempo de espera entre la entrada y salida al cuarto

    def salir(self):
        Estudiante.estudiantesin -= 1
        print("Estudiante fuera")


class Semaforo:
    def __init__(self, n):
        self.semaforo = threading.Semaphore(n)

    def wait(self):
        self.semaforo.acquire()

    def signal(self):
        self.semaforo.release()


decano = Decano()  # Un único decano
mutuo = Semaforo(1)
lleno_vacio = Semaforo(0)
entrada = Semaforo(1)


def decano_thread():
    mutuo.wait()
    if 0 < Estudiante.estudiantesin < 50:
        decano.esperar()
        mutuo.signal()
        lleno_vacio.wait()  # Espera a que los estudiantes sean 50 o cero

    if Estudiante.estudiantesin >= 50:
        decano.interrumpir_fiesta()
        entrada.wait()  # Bloquea la entrada a mas estudiantes
        mutuo.signal()
        lleno_vacio.wait()  # Espera a que todos los estudiantes se vayan
        entrada.signal()  # Vuelve a habilitar el paso a los estudiantes
    else:
        decano.iniciar_busqueda()

    decano.salir()
    mutuo.signal()


def estudiante_thread():
    mutuo.wait()
    estudiante = Estudiante()
    if decano.dentro:
        mutuo.signal()
        entrada.wait()  # Esperar hasta que el decano se vaya
        entrada.signal()
        mutuo.wait()

    estudiante.entrar()
    if Estudiante.estudiantesin == 50 and not decano.dentro:
        lleno_vacio.signal()
    else:
        mutuo.signal()  # Pasar relevo a otro estudiante o al decano

    estudiante.fiesta()
    mutuo.wait()
    estudiante.salir()
    if Estudiante.estudiantesin == 0:
        lleno_vacio.signal()
    mutuo.signal()


def main():
    decano_t = threading.Thread(target=decano_thread)

    for i in range(100):
        if i == 45:  # Se puede variar en qué momento entra el decano (i = 0, i > 50)
            decano_t.start()
        e = threading.Thread(target=estudiante_thread)
        e.start()

if __name__ == '__main__':
    main()
