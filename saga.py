import requests
import requests.exceptions

def book_trip(flight_details, hotel_details, car_details):
    flight_response = hotel_response = car_response = {}
    try:
        print("Intentando reservar vuelo...")
        flight_response = requests.post('http://localhost:5001/book', json=flight_details).json()
        if flight_response['status'] != 'success':
            print( Exception('Reserva de vuelo fallida'))
        # Imprime detalles del vuelo indicando origen y destino
        print(f"Vuelo reservado con éxito! Origen: {flight_details['origin']}, Destino: {flight_details['destination']}")

        print("Intentando reservar hotel...")
        hotel_response = requests.post('http://localhost:5002/book', json=hotel_details).json()
        if hotel_response['status'] != 'success':
            raise Exception('Reserva de hotel fallida')
        # Imprime detalles del hotel indicando nombre y noches
        print(f"Hotel reservado con éxito! Nombre: {hotel_details['name']}, Noches: {hotel_details['nights']}")

        print("Intentando reservar auto...")
        car_response = requests.post('http://localhost:5003/book', json=car_details).json()
        if car_response['status'] != 'success':
            print( 'Reserva de autos fallida')
        # Imprime detalles del auto indicando tipo y días
        print(f"Auto reservado con éxito! Tipo: {car_details['type']}, Días: {car_details['days']}")

        print("¡Viaje reservado con éxito!")
        return flight_response['booking_id'], hotel_response['booking_id'], car_response['booking_id']
    except requests.exceptions.ConnectionError as e:
        print("-----------------------------------------------------------")
        print("-  ¡¡Se ha producido un error al realizar las reservas!!  -")
        print("-----------------------------------------------------------")
        # Si algo falla, iniciamos el proceso de compensación
        if 'booking_id' in flight_response:
            print("Ejecutando proceso de compensación para el vuelo...")
            requests.post('http://localhost:5001/cancel', json={'booking_id': flight_response['booking_id']})
        if 'booking_id' in hotel_response:
            print("Ejecutando proceso de compensación para el hotel...")
            requests.post('http://localhost:5002/cancel', json={'booking_id': hotel_response['booking_id']})
        if 'booking_id' in car_response:
            print("Ejecutando proceso de compensación para el auto...")
            requests.post('http://localhost:5003/cancel', json={'booking_id': car_response['booking_id']})
        print(f"Detalles del error: {str(e)}")
        

# Uso:
flight_details = {"origin": "NYC", "destination": "LAX"}
hotel_details = {"name": "Hotel California", "nights": 3}
car_details = {"type": "SUV", "days": 3}

try:
    booking_ids = book_trip(flight_details, hotel_details, car_details)
except Exception as e:
     print("Error al realizar las reservas. Por favor, inténtelo de nuevo más tarde.")
