import os, datetime

def numberValidate(number, type):
  match type:
    case 'float': chars = '0123456789.'
    case 'int': chars = '0123456789'
  
  for char in number:
    if char not in chars: return False
  return True

def yesOrNoValidate(str):
   chars = 'SN'
   if ((str.upper() not in chars) or len(str) > 1): return False
   return True
def strValidate(str):
  str = str.upper()
  chars = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ '
  for char in str:
    if char.upper() not in chars: return False
  return True
#1)- Interfaz
def dataGenerator():
    data = []
    waste = 0 #margen de desperdicio por defecto (en caso de que no se ingrese otro valor posteriormente)
    clientName = input('Nombre del cliente:\n\t=> ')
    while(not(strValidate(clientName))): clientName = input('¡ERROR!\nIngrese un nombre válido.\n\t=> ')
    #unidad con la que se trabajará... (metros, pies, centimetros, kilometros, yardas...)
    while True:
      unitOfMeasure = input('Unidad de medida de registro de los datos de la superficie:\n1-Metros\n2-Pies\n3-Kilómetros\n4-Centímetros\n5-Yardas\n\t=> ')
      if not unitOfMeasure.isnumeric():
        print('\n¡ERROR!\nIngrese una opción válida.\n')
      else:
         if (not(numberValidate(unitOfMeasure, 'int'))): unitOfMeasure = print('\n¡ERROR!\nIngrese una opción válida.\n')
         else:
          if 1<=int(unitOfMeasure) and int(unitOfMeasure)<=5: break
          else: print('\n¡ERROR!\nIngrese una opción válida.\n')  
    #confirmación de unidad de medida
    match unitOfMeasure:
      case int(1): print('\n--Unidad de medida: METROS CÚBICOS [m³]--\n')
      case int(2): print('\n--Unidad de medida: PIES CÚBICOS [ft³]--\n')
      case int(3): print('\n--Unidad de medida: KILÓMETROS CÚBICOS [km³]--\n')
      case int(4): print('\n--Unidad de medida: CENTÍMETROS CÚBICOS [cm³]--\n')
      case int(5): print('\n--Unidad de medida: YARDAS CÚBICAS [yd³]--\n') 
    length = input('Longitud de la superficie:\n\t=> ')
    while(not(numberValidate(length, 'float') and float(length) > 0 )): length = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    width = input('Ancho de la superficie:\n\t=> ')
    while(not(numberValidate(width, 'float') and float(width) > 0)): width = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    height = input('Altura de la superficie:\n\t=> ')
    while(not(numberValidate(height, 'float') and float(height) > 0 )): height = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    wasteMargin = input('¿Se utilizará un margen de desperdicio para el material?\n!(S / N)\n\t=> ')
    while(not(yesOrNoValidate(wasteMargin))): wasteMargin = input('¡Respuesta inválida!\n\t=> ')
    if (wasteMargin.upper() == 'S'): 
       waste = input('Margen de desperdicio de hormigón:\n\t=> ')
       while(not(numberValidate(waste, 'float'))): waste=input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    density = input('Densidad deseada del material:\n\t=> ')
    while (not(numberValidate(density, 'float'))): density = input('¡ERROR!\nIngrese una cantidad válida.\n\t=> ')
    data.append(float(length))
    data.append(float(width))
    data.append(float(height))
    data.append(float(density))
    data.append(float(waste)/100 if float(waste) > 0 else 0)#calculo del valor % para utilizarlo de forma directa => 10% = 0.1
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
    return (f'\t✔️ Fecha de pedido: {dateFormatted}\n\t✔️ Cliente: {name}\n\t✔️ Cantidad de material solicitado: {amountOfMaterial} metros cúbicos (m³)')

def ticketGenerator (data, calc):
    wasteResponse = (f'{(data[4]*100)}%' if data[4] >0 else 'N/A') #uso de operaciones ternarias para definir el valor final
    densityResponse = (f'{data[3]}kg/m³' if data[3] > 0 else 'N/A')
    weightResponse = (f'{calc[3]}kg' if calc[3] > 0 else '"Sin densidad definida"')
    ticketData = (f'\n---INFORMACIÓN DE PEDIDO---\n\nCliente: {data[5]}\n*Superficie solicitada:\n\t1-Longitud: {data[0]}\n\t2-Ancho: {data[1]}\n\t3-Altura: {data[2]}\n*Material\n\t1-Cantidad solicitada: {calc[1]}m³\n\t2-Peso: {weightResponse}\n*Datos sobre el material:\n\t1-Densidad utilizada: {densityResponse}\n\t2-Margen de desperdicio: {wasteResponse}')
    try:
      with open('ticket.txt', 'w') as file:
        file.write(ticketData)
      print(ticketData)
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
     with open('orderHistory.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
        for row in data:
           print(row)
  except FileNotFoundError: print('\nNo hay ventas registradas\n') 
  
  area = dataGenerator()
  result = calculate(area)
  addOrder(orderData(result[0], result[1]))
  ticketResponse = input('¿Desea generar el ticket del cliente registrado?\n\t=> ')
  while(not(yesOrNoValidate(ticketResponse))): ticketResponse = input('¡ERROR!\nIngrese una respuesta válida (S / N)\n\t=> ')
  if (ticketResponse.upper() == 'S'):
     ticketGenerator(area, result)

main()