import time
from mozio_api import MozioApi

DELAY_BEFORE_POLLING_IN_SECONDS = 1


def main():
    api_obj = MozioApi()

    # Sample search request body
    search_query = {
        'start_address': '44 Tehama Street, San Francisco, CA, USA',
        'end_address': 'SFO',
        'mode': 'one_way',
        'pickup_datetime': '2023-12-05 19:30',
        'num_passengers': 2,
        'currency': 'USD',
        'campaign': 'Emirhan Oguz'
    }
    create_search_res = api_obj.create_search(search_query)
    if not create_search_res['success']:
        print('\nSomething went wrong on creating a search. Details:\n'
              + create_search_res['data'])
        exit()

    search_id = create_search_res['data']
    print('\nYour search created successfully! Search id: ' + search_id)

    time.sleep(DELAY_BEFORE_POLLING_IN_SECONDS)
    poll_search_result = api_obj.get_search_poll(search_id)
    if not poll_search_result['success']:
        print('\nSomething went wrong on polling the search result. Details:\n'
              + poll_search_result['data'])
        exit()

    print('\nYour search results polled successfully! Search id: ' + search_id)
    search_result = poll_search_result['data']
    cheapest_test_result = None
    cheapest_price = float('inf')
    for result in search_result:
        steps = result['steps']
        for step in steps:
            provider = step['details']['provider']
            price = float(step['details']['price']['price']['value'])
            if provider['name'] == 'Dummy External Provider' and price < cheapest_price:
                cheapest_test_result = result
                break

    if cheapest_test_result is None:
        print('\nThere is no test result for Dummy External Provider')
        exit()

    # Sample reservation request body
    reservation_data = {
        'search_id': search_id,
        'result_id': cheapest_test_result['result_id'],
        'email': 'emirhanoguz@gmail.com',
        'country_code_name': 'TR',
        'phone_number': '5551112233',
        'first_name': 'Emirhan',
        'last_name': 'Oguz',
        'airline': 'AA',
        'flight_number': '123',
        'customer_special_instructions': 'Lorem ipsum dolar sit amet',
    }

    book_reservation = api_obj.book_reservation(reservation_data)
    if not book_reservation['success']:
        print('\nSomething went wrong on booking reservation. Details:\n'
              + book_reservation['data'])
        exit()

    print('\nYour reservation is in progress...')
    reservation_result = api_obj.get_booking_poll(search_id)

    if not reservation_result['success']:
        print('\nSomething went wrong on getting reservation result. Details:\n'
              + reservation_result['data'])
        exit()

    print('\nYour reservation booked successfully!\nReservation details:')

    reservation_list = reservation_result['data']
    for reservation in reservation_result['data']:
        print('\n-----------------------------------')
        print('Reservation id: ' + reservation['id'] + '\n'
              + 'URL: ' + reservation['url'] + '\n'
              + 'Paid Amount: ' + reservation['amount_paid'] + '\n'
              + 'Gratuity: ' + reservation['gratuity'] + '\n'
              + 'Campaign: ' + reservation['campaign'] + '\n'
              + 'Confirmation Number: ' + reservation['confirmation_number'] + '\n'
              + 'Phone Number: ' + reservation['phone_number'] + '\n'
              + 'Departure Time: ' + reservation['voyage']['departure_datetime'] + '\n'
              + 'Special Instructions: ' + reservation['customer_special_instructions'] + '\n')

    for reservation in reservation_list:
        reservation_id = reservation['id']
        cancel_booking = api_obj.cancel_booking(reservation_id)
        if not cancel_booking['success']:
            print('\nSomething went wrong on canceling your reservation. Details:\n'
                  + cancel_booking['data'])
            exit()
        print('Your cancellation is successful for the reservation id: ' + reservation_id)


if __name__ == '__main__':
    main()