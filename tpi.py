#ENTRADA => Dimensiones de la superficie a trabajar (Longitud, anchura y altura) 
#SALIDA => Total de material (Hormigón) necesario para rellenar la superficie a trabajar

def data():
    data = []
    length = input('Ingrese la longitud de la superficie:\n')
    width = input('Ingrese el ancho de la superficie:\n')
    height = input('Ingrese la altura de la superficie:\n')
    data.append(length)
    data.append(width)
    data.append(height)
    return data

def calculate(length, width, height):
    amount = int(length) * int(width) * int(height) #cantidad de material necesario = mts3
    return round(amount, 2)

def showData (surfaceDate, amountOfMaterial):
    return (f'---INFORMACIÓN DE LA SUPERFICIE---\n\t1-Longitud: {surfaceDate[0]}\n\t2-Ancho: {surfaceDate[1]}\n\t3-Altura: {surfaceDate[2]}\nRTA: La cantidad de hormigon que necesitará para cubrir la superficie serán {amountOfMaterial} metros cúbicos (m³)')

def add():
    with open ('order.txt', 'a') as file:
        information = showData(surface, calculate(surface[0], surface[1], surface[2]))
        file.write(information)
        file.write('\t-'*20+'\n')
surface = data()
showData(surface, calculate(surface[0], surface[1], surface[2]))
add()