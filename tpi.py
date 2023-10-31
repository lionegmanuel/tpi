import os, datetime

def floatValidate(number):
  chars = '0123456789.'
  for char in number:
    if char not in chars: return False
  return True

def yesOrNoValidate(str):
   chars = 'SN'
   if ((str.upper() not in chars) or len(str) > 1): return False
   return True
def strValidate(str):
  str = str.upper()
  chars = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
  for char in str:
    if char.upper() not in chars: return False
  return True
#1)- Interfaz
def dataGenerator():
    data = []
    clientName = input('Nombre del cliente:\n\t=> ')
    while(not(strValidate(clientName))): clientName = input('¡ERROR!\nIngrese un nombre válido.\n\t=> ')
    length = input('Longitud de la superficie:\n\t=> ')
    while(not(floatValidate(length))): length = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    width = input('Ancho de la superficie:\n\t=> ')
    while(not(floatValidate(width))): width = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    height = input('Altura de la superficie:\n\t=> ')
    while(not(floatValidate(height))): height = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    wasteMargin = input('¿Se utilizará un margen de desperdicio para el material?\n!(S / N)\n\t=> ')
    while(not(yesOrNoValidate(wasteMargin))): wasteMargin = input('¡Respuesta inválida!\n\t=> ')
    if (wasteMargin.upper() == 'S'): 
       waste = input('Margen de desperdicio de hormigón:\n\t=> ')
       while(not(floatValidate(waste))): waste=input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    density = input('Densidad deseada del material:\n\t=> ')
    while (not(floatValidate(density))): density = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    data.append(float(length))
    data.append(float(width))
    data.append(float(height))
    data.append(float(density))
    data.append(float(waste)/100)#calculo del valor % para utilizarlo de forma directa => 10% = 0.1
    data.append(clientName)
    return data

#2)- Núcleo Lógico y control de resultados 
def calculate(clientData):
    amount = round((clientData[0] * clientData[1] * clientData[2]),2) #cantidad de material necesario = mts3
    if (clientData[4]!=0):
       amount = amount * (1+clientData[4])
    if (clientData[3]!=0): weight = amount * clientData[3] #m3 / kg/m3 => peso
    else: weight = 0    
    return [clientData[5], round(amount,2), (clientData[4]*100), round(weight,1)]

def orderData (name, amountOfMaterial):
    currentDate = datetime.datetime.now()
    dateFormatted = currentDate.strftime('%Y-%m-%d %H:%M:%S')
    return (f'---HISTORIAL---\n\t✔️ Fecha de pedido: {dateFormatted}\n✔️ Cliente: {name}\n✔️ Cantidad de material solicitado: {amountOfMaterial} metros cúbicos (m³)')

def ticketGenerator (data, calc):
    data = (f'---INFORMACIÓN DE PEDIDO---\nCliente: {data[5]}\n*Superficie solicitada:\n\t1-Longitud: {data[0]}\n\t2-Ancho: {data[1]}\n\t3-Altura: {data[2]}\n*Material\n\t1-Cantidad solicitada: {calc[1]} metros cúbicos (m³)\n\t2-Peso: {calc[3]}kg\n*Datos sobre el material:\n\t1-Densidad utilizada: {data[3]}\n\t2-Margen (%) de desperdicio: {(data[4]*100)}')
    try:
      with open('ticket.txt', 'w') as file:
        file.write(data)
      print(data)
    except: print('Ocurrió un error al generar el ticket.')        

#3)- Gestión de Archivos / Registros / Pedidos
def addOrder(order):
  try:  
    with open ('orderHistory.txt', 'a', encoding='utf-8') as file:
        file.write(order)
        file.write('\n' + '-'*20 + '\n') #linea en blanco
    print('\nPedido registrado con éxito.\n')
  except Exception as e: print(f'\n--ERROR al registrar el pedido--\n{e}')
#datos de ingreso
def main():
  #historial previo
  try:
     print('--HISTORIAL DE VENTAS--')
     with open('orderHistory.txt', 'r') as file:
        data = file.readlines()
        for row in data:
           print(data[row])
  except FileNotFoundError: print('\nNo hay ventas registradas\n') 
  
  area = dataGenerator()
  result = calculate(area)
  addOrder(orderData(result[0], result[1]))
  ticketResponse = input('¿Desea generar el ticket del cliente registrado?\n\t=> ')
  while(not(yesOrNoValidate(ticketResponse))): ticketResponse = input('¡ERROR!\nIngrese una respuesta válida (S / N)\n\t=> ')
  if (ticketResponse.upper() == 'S'):
     ticketGenerator(area, result)

main()