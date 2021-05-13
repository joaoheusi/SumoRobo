import ufirebase as firebase
import network
import machine
import gc

gc.collect()

ssid = "wifi" #Nome da rede Wifi
password = "senha" #senha do Wifi
FREQUENCIA_MOTOR = 50
INICIO_OPERACAO_MOTOR = 40
MAXIMO_OPERACAO_MOTOR = 115


station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,password)

#Aguarda enquanto wifi é conectado
while station.isconnected() == False:
  pass

print("Wifi conectado")
print(station.ifconfig())

def valor_relativo(given, relative, start=INICIO_OPERACAO_MOTOR,end=MAXIMO_OPERACAO_MOTOR):
  #Recebe um valor de 0 a 50 e retorna o valor correto para a faixa do motor utilizado
  numSteps = MAXIMO_OPERACAO_MOTOR - INICIO_OPERACAO_MOTOR
  stepSize = numSteps/50
  relative = start + given*stepSize
  return relative


#ALTERAR PINAGEM PARA A UTILIZADA
leftPwm1 = machine.PWM(machine.Pin((31)), freq = FREQUENCIA_MOTOR) # PWM 1 RODA ESQUERDA - GIRA PARA TRÁS
leftPwm2 = machine.PWM(machine.Pin((31)), freq = FREQUENCIA_MOTOR) # PWM 2 RODA ESQUERDA - GIRA PARA FRENTE
rightPwm1 = machine.PWM(machine.Pin((31)), freq = FREQUENCIA_MOTOR) # PWM 1 RODA DIREITA - GIRA PARA TRÁS
rightPwm2 = machine.PWM(machine.Pin((31)), freq = FREQUENCIA_MOTOR) # PWM 2 RODA DIREITA - GIRA PARA FRENTE

while True:
  leftPwm1Value = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/leftWeelPwm1.json")
  leftPwm2Value = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/leftWeelPwm2.json")
  rightPwm1Value = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/rightWeelPwm1.json")
  rightPwm2Value = firebase.get("https://sumorobo-esp-heusi-default-rtdb.firebaseio.com/SumoRoboEsp/righttWeelPwm2.json")
  
  #Zerando valores pra não ocorrer curto
  leftPwm1.duty(INICIO_OPERACAO_MOTOR)
  leftPwm2.duty(INICIO_OPERACAO_MOTOR)
  rightPwm1.duty(INICIO_OPERACAO_MOTOR)
  rightPwm2.duty(INICIO_OPERACAO_MOTOR)

  leftPwm1.duty(valor_relativo(leftPwm1Value))
  leftPwm2.duty(valor_relativo(leftPwm2Value))
  rightPwm1.duty(valor_relativo(rightPwm1Value))
  rightPwm2.duty(valor_relativo(rightPwm2Value))


