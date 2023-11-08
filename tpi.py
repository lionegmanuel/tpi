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
def unitOfMeasureConvertion(value, origin ,destination):
  newValue = 0
  if (destination == 'mt'): #=> conversion de unidades para tarbajar con el sistema interno hacia metros cubicos
     match origin:
        case 'ft': newValue = value * 0.02831685
        case 'yd': newValue = value * 0.7645549
        case 'km': newValue = value * 1000000000 
        case 'cm': newValue = value * 0.000001
  else:
     match destination: #=> conversion de unidades a nivel externo para mostrar los resultados (en el sistema que ingresó el usuario si es que es != metros cubicos)
        case 'ft': newValue = value * 35.315
        case 'yd': newValue = value * 1.307951
        case 'km': newValue = value * 0.000000001
        case 'cm': newValue = value * 1000000
  return round(newValue,2)
#1)- Interfaz

def dataGenerator():
    data = []
    waste = 0 #margen de desperdicio por defecto (en caso de que no se ingrese otro valor posteriormente)
    clientName = input('Nombre del cliente:\n\t=> ')
    while(not(strValidate(clientName))): clientName = input('¡ERROR!\nIngrese un nombre válido.\n\t=> ')
    #unidad con la que se trabajará... (metros, pies, centimetros, kilometros, yardas...)
    unitOfMeasure = ''
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
    strUnitOfMeasure = 'mt'
    match unitOfMeasure:
      case '1': 
        print('\n--Unidad de medida: METROS CÚBICOS [m³]--\n')
      case '2': 
        print('\n--Unidad de medida: PIES CÚBICOS [ft³]--\n')
        strUnitOfMeasure = 'ft'
      case '3': 
        print('\n--Unidad de medida: KILÓMETROS CÚBICOS [km³]--\n')
        strUnitOfMeasure = 'km'
      case '4': 
        print('\n--Unidad de medida: CENTÍMETROS CÚBICOS [cm³]--\n')
        strUnitOfMeasure = 'cm'
      case '5':
        print('\n--Unidad de medida: YARDAS CÚBICAS [yd³]--\n') 
        strUnitOfMeasure = 'yd'

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
    data.append(strUnitOfMeasure)
    return data

#2)- Núcleo Lógico y control de resultados 
def calculate(clientData):
    #conversion de las unidades de medida a nivel interno => pasaje neto a metros cúbicos
  if (clientData[6] != 'mt'):
      clientData[0] = unitOfMeasureConvertion(clientData[0], clientData[6], 'mt')
      clientData[1] = unitOfMeasureConvertion(clientData[1], clientData[6], 'mt')
      clientData[2] = unitOfMeasureConvertion(clientData[2], clientData[6], 'mt')

  #calculos normales (en metros cúbicos)
  amount = round((clientData[0] * clientData[1] * clientData[2]),2) #cantidad de material necesario
  if (clientData[4]!=0):
    amount = amount * (1+clientData[4])
  if (clientData[3]!=0): weight = round(amount * clientData[3],1) #m3 / kg/m3 => peso
  else: weight = 0    
  return [clientData[5], amount, (clientData[4]*100), weight]

def orderData (name, amountOfMaterial):
    currentDate = datetime.datetime.now()
    dateFormatted = currentDate.strftime('%Y-%m-%d %H:%M:%S')
    return (f'\t✔️ Fecha de pedido: {dateFormatted}\n\t✔️ Cliente: {name}\n\t✔️ Cantidad de material solicitado: {amountOfMaterial} metros cúbicos (m³)')

def ticketGenerator (data, calc):
    print(f'Longitud de "DATA" en ticket generator: {len(data)}')
    #formato de respuestas != de la superficie
    wasteResponse = (f'{(data[4]*100)}%' if data[4] >0 else 'N/A') #uso de operaciones ternarias para definir el valor final
    densityResponse = (f'{data[3]}kg/m³' if data[3] > 0 else 'N/A')
    weightResponse = (f'{calc[3]}kg' if calc[3] > 0 else '"Sin densidad definida"')
    amountResponse = (f'{calc[1]}m³')
    lengthResponse = (f'{data[0]}m³')
    widthResponse = (f'{data[1]}m³')
    heightResponse = (f'{data[2]}m³')
    #conversion de las unidades de medida
    if (data[6] != 'mt'):
      aditionalValue = unitOfMeasureConvertion(calc[1], "mt", data[6]) #cálculo del valor adicional a mostrar en la unidad de medida 
      newLengthValue = unitOfMeasureConvertion(data[0], "mt", data[6])
      newWidthValue = unitOfMeasureConvertion(data[1], "mt", data[6])
      newHeightValue = unitOfMeasureConvertion(data[2], "mt", data[6])
      #deseada del cliente
      match data[6]:
        case 'ft': 
          aditionalResponse = f'{aditionalValue}ft³'
          lengthResponse = f'{newLengthValue}ft³'
          widthResponse = f'{newWidthValue}ft³'
          heightResponse = f'{newHeightValue}ft³'
        case 'yd':
          aditionalResponse = f'{aditionalValue}yd³'
          lengthResponse = f'{newLengthValue}yd³'
          widthResponse = f'{newWidthValue}yd³'
          heightResponse = f'{newHeightValue}yd³'
        case 'cm':
          aditionalResponse = f'{aditionalValue}cm³'
          lengthResponse = f'{newLengthValue}cm³'
          widthResponse = f'{newWidthValue}cm³'
          heightResponse = f'{newHeightValue}cm³'
        case 'km':
          aditionalResponse = f'{aditionalValue}km³'  
          lengthResponse = f'{newLengthValue}km³'
          widthResponse = f'{newWidthValue}km³'
          heightResponse = f'{newHeightValue}km³'
      amountResponse+=f' / {aditionalResponse}'
    
    ticketData = (f'\n---INFORMACIÓN DE PEDIDO---\n\nCliente: {data[5]}\n\n*Superficie solicitada:\n\t1-Longitud: {lengthResponse}\n\t2-Ancho: {widthResponse}\n\t3-Altura: {heightResponse}\n*Material\n\t1-Cantidad necesaria: {amountResponse} \n\t2-Peso: {weightResponse}\n*Datos sobre el material:\n\t1-Densidad utilizada: {densityResponse}\n\t2-Margen de desperdicio: {wasteResponse}')
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
  tittle = 'SISTEMA DE CÁLCULO DE HORMIGÓN'
  print('=' * len(tittle))
  print(tittle)
  print('=' * len(tittle))
  #historial previo
  try:
     print('\n--HISTORIAL DE CLIENTES & PEDIDOS--\n')
     with open('orderHistory.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
        for row in data:
           print(row)
  except FileNotFoundError: print('No hay un registro de pedidos / clientes existente para mostrar.\n') 
  
  area = dataGenerator()
  result = calculate(area)
  addOrder(orderData(result[0], result[1]))
  ticketResponse = input('¿Desea generar el ticket del cliente registrado?\n\t=> ')
  while(not(yesOrNoValidate(ticketResponse))): ticketResponse = input('¡ERROR!\nIngrese una respuesta válida (S / N)\n\t=> ')
  if (ticketResponse.upper() == 'S'):
     ticketGenerator(area, result)

main()