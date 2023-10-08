import requests

def book_trip(flight_details, hotel_details, car_details):
    flight_response = hotel_response = car_response = {}
    try:
        print("Intentando reservar vuelo...")
        flight_response = requests.post('http://localhost:5001/book', json=flight_details).json()
        if flight_response['status'] != 'success':
            raise Exception('Reserva de vuelo fallida')
        print("Vuelo reservado con éxito!")

        print("Intentando reservar hotel...")
        hotel_response = requests.post('http://localhost:5002/book', json=hotel_details).json()
        if hotel_response['status'] != 'success':
            raise Exception('Reserva de hotel fallida')
        print("Hotel reservado con éxito!")

        print("Intentando reservar auto...")
        car_response = requests.post('http://localhost:5003/book', json=car_details).json()
        if car_response['status'] != 'success':
            raise Exception('Reserva de autos fallida')
        print("Auto reservado con éxito!")

        print("¡Viaje reservado con éxito!")
        return flight_response['booking_id'], hotel_response['booking_id'], car_response['booking_id']
    except Exception as e:
        print(f"Error: {e}")
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
        raise e

# Uso:
flight_details = {"origin": "NYC", "destination": "LAX"}
hotel_details = {"name": "Hotel California", "nights": 3}
car_details = {"type": "SUV", "days": 3}

try:
    booking_ids = book_trip(flight_details, hotel_details, car_details)
except Exception as e:
    print(f"Error al realizar las reservas: {e}")
