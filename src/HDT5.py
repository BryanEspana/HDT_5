'''
Hoja de Trabajo #5 
Bryan Carlos Roberto España Machorro - 21550
Algoritmos y Estructura de Datos
Catedratico Moises Alonso
Aux: Cristian Laynez y Rudik Rompich

'''
import simpy
import random
import time

#Inicio de tiempo de corrida
inicio = time.time()
#Bienvenida
print('----------------Simulador de RAM----------------')
print('-----------------Ejecutando CPU-----------------')

#Funcion de Simulador
def simulation(name, env, memory, cpu, RunInicial, ProcesosInstruction, ram):
    #Simula la bienvenida del proceso
    yield env.timeout(RunInicial)
    #Coloca el tiempo que simulo
    TimeRunInicial = env.now
    #Instrucción [NEW] cuando se ingresa un proceso nuevo 
    print('%s en [NEW] en cola: %d \nCantidad de ram requerida: %d, RAM disponible:  %d' % (name, env.now, ram, memory.level))
    yield memory.get(ram)
    #Repetir hasta que se acaben los procesos
    while ProcesosInstruction > 0: 
        #Instrucción [READY] cuando pasa de NEW a utilizarlo
        print('%s en [READY] En tiempo: %d\nProgramas pendientes %d' % (name, env.now, ProcesosInstruction))
        #Empieza a correr los programas [RUNING]
        with cpu.request() as req:
            yield req
            ProcesosInstruction = ProcesosInstruction - 3
            #Simulador de ciclo 
            yield env.timeout(1) 
            #Creación del procesador
            print('%s en [RUNNING] En tiempo: %d\nCantidad de ram: %d, procesos pendientes: %d RAM disponible: %d' % (name, env.now, ram, ProcesosInstruction, memory.level))
            #Si no hay ningun proceso selecciona el otro if
            if  ProcesosInstruction >= 0:
                numeroRandom = random.randint(1, 2)
                if numeroRandom == 1:
                    #Imprime el [WAITING] del proceso que esta en espera
                    yield env.timeout(1)
                    print('%s en [WAITING] En tiempo: %d\nCantidad ram %d, Procesos pendientes %d RAM disponible: %d' % (name, env.now, ram, ProcesosInstruction, memory.level))
                else:
                    pass
            else:
                #Devuelve ram utilizada
                yield memory.put(ram)

                #Instrucción [TERMINATED] 
                print('%s en [TERMINATED] en tiempo: %d\ncantidad FINAL de ram: %d, Nueva cantidad de RAM: %d' % (name, env.now, ram, memory.level))
                global timeTotal
                timeTotal += env.now - TimeRunInicial
                print('Tiempo total %d' % (env.now - TimeRunInicial))
#Variables Necesarias
random.seed(10)
env = simpy.Environment()  # Crea la simulación
ramInicial = simpy.Container(env, 100, init=100)  #Crea el contador de la RAM
cpuInicial = simpy.Resource(env, capacity=1)  #Crea el simulador del "procesador" con capacidad de 1
processInicial = 2 #cantidad de procesos que genera el procesador
timeTotal = 0


for i in range(processInicial):
    RunInicial = 0
    #Tiempo en el que inician todas las aplicaciones (0)
    ProcesosInstruction = random.randint(1, 200)  
    #Operaciones realizadas entre 1 y 25 aleatoriamente
    ramUtilizada = random.randint(1, 10)
    #Cantidad de Ram por cada proceso
    env.process(simulation('Programa %d' % i, env, ramInicial, cpuInicial, RunInicial, ProcesosInstruction, ramUtilizada))

#Corre la simulación
env.run()
print('Tiempo total del promedio: %d ' % (timeTotal / processInicial))
#Finalización de tiempo de corrida
fin = time.time()
print('---------Saliendo del Simulador de RAM----------')
print('El tiempo que tardo en ejecutar son',fin-inicio, 'microsengudos')
