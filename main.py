import ufirebase as firebase
import network
import machine
import gc

gc.collect()

ssid = "wifi" #Nome da rede Wifi
password = "senha" #senha do Wifi
FREQUENCIA_MOTOR = 50
INICIO_OPERACAO_MOTOR = 0
MAXIMO_OPERACAO_MOTOR = 100


station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,password)

#Aguarda enquanto wifi é conectado
while station.isconnected() == False:
  pass

print("Wifi conectado")
print(station.ifconfig())

def valor_relativo(given, start=INICIO_OPERACAO_MOTOR,end=MAXIMO_OPERACAO_MOTOR):
  #Recebe um valor de 0 a 50 e retorna o valor correto para a faixa do motor utilizado]
  relative = 0
  numSteps = MAXIMO_OPERACAO_MOTOR - INICIO_OPERACAO_MOTOR
  stepSize = numSteps/50
  relative = start + given*stepSize
  return relative


#ALTERAR PINAGEM PARA A UTILIZADA
leftPwm = machine.PWM(machine.Pin((31)), freq = FREQUENCIA_MOTOR) # PWM 1 RODA ESQUERDA - CONTROLA VELOCIDADE
leftA = machine.Pin(31, machine.Pin.OUT)
leftB = machine.Pin(31, machine.Pin.OUT)

rightPwm = machine.PWM(machine.Pin((31)), freq = FREQUENCIA_MOTOR) # PWM 2 RODA DIREITA - CONTROLA VELOCIDADE
rightA = machine.Pin(31, machine.Pin.OUT)
rightB = machine.Pin(31, machine.Pin.OUT)

while True:

  leftPwmValue = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/leftWeelPwm.json")
  rightPwmValue = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/rightWeelPwm.json")
  rightAValue = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/rightWeelA.json")
  leftAValue = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/leftWeelA.json")
  rightBValue = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/rightWeelB.json")
  leftBValue = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/leftWeelB.json")
  

  leftPwm.duty(valor_relativo(int(leftPwmValue)))
  rightPwm.duty(valor_relativo(int(rightPwmValue)))
  rightA.value(int(rightAValue))
  rightB.value(int(rightBValue))
  leftA.value(int(leftAValue))
  leftB.value(int(leftBValue))


