
import random
import json
import sys

# Definimos los Arcanos Mayores
arcanos_mayores = [
    'El Mago', 'La Sacerdotisa', 'La Emperatriz', 'El Emperador',
    'El Hierofante', 'Los Enamorados', 'El Carro', 'La Justicia',
    'El Ermitaño', 'La Rueda de la Fortuna', 'La Fuerza', 'El Colgado',
    'La Muerte', 'La Templanza', 'El Diablo', 'La Torre',
    'La Estrella', 'La Luna', 'El Sol', 'El Juicio', 'El Mundo', 'El Loco'
]

# Función para generar los Arcanos Menores
def generar_arcanos_menores():
    palos = ['Bastos', 'Copas', 'Espadas', 'Oros']
    figuras = ['As', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete', 'Ocho', 'Nueve', 'Diez', 'Sota', 'Caballo', 'Reina', 'Rey']
    arcanos_menores = []

    for palo in palos:
        for figura in figuras:
            arcanos_menores.append(f'{figura} de {palo}')

    return arcanos_menores

# Añadimos los Arcanos Menores a los Mayores para tener la lista completa de cartas de tarot
tarot_cards = arcanos_mayores + generar_arcanos_menores()

# Función para simular la tirada de tarot
def tarot_reading(spread):
    reading = {'cards': []}
    number_of_cards = 1  # Por defecto una carta

    if spread == 'three-card':
        number_of_cards = 3
    elif spread == 'celtic-cross':
        number_of_cards = 10
    elif spread == 'single-card':  # Añadido para permitir la tirada de una sola carta
        number_of_cards = 1

    # Aseguramos que las cartas no se repitan en una tirada
    selected_cards = random.sample(tarot_cards, number_of_cards)
    
    for card in selected_cards:
        position = random.choice(['upright', 'reversed'])
        reading['cards'].append({'name': card, 'position': position})

    return reading

# Esta sería la función que recibiría la llamada de GPT-4
def function_calling(spread_type):
    # Obtenemos el resultado de la tirada
    reading_result = tarot_reading(spread_type)
    
    # Convertimos el resultado a JSON para la salida
    print(json.dumps(reading_result))

if __name__ == "__main__":
    # Tomamos el tipo de tirada desde la línea de comandos
    if len(sys.argv) < 2:
        print("Uso: python tarot.py [single-card | three-card | celtic-cross]")
    else:
        spread_type = sys.argv[1]
        function_calling(spread_type)
