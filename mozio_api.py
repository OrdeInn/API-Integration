import requests
import time
import json
from dotenv import dotenv_values

# Load the API Key from .env file
env_vars = dotenv_values()
api_key = env_vars['MOZIO_API_KEY']

class MozioAPI:
    def __init__(self):
        self.api_key = api_key
        self.base_url = 'https://api-testing.mozio.com/v2'
        self.headers = {'Api-Key': self.api_key}

    def createSearch(self, search_data):
        url = self.base_url + '/search/'
        response = requests.post(url, headers = self.headers, json = search_data)
        result = {
            'success': False,
            'data': ''
        }
        if response.status_code != requests.codes.created:
            result['data'] = json.dumps(response.json())
            return result

        response = response.json()
        result['success'] = True
        result['data'] = response['search_id']
        return result
            
    def getSearchPoll(self, search_id):
        url = self.base_url + '/search/' + search_id + '/poll/'
        result_list = []
        more_coming = True
        result = {
            'success': False,
            'data': ''
        }
        while (more_coming):
            response = requests.get(url, headers = self.headers)
            if (response.status_code != requests.codes.accepted and
                response.status_code != requests.codes.ok):
                result['data'] = json.dumps(response.json())
                break

            response = response.json()
            more_coming = bool(response['more_coming'])
            result_list += (response['results'])

            if (more_coming):
                time.sleep(2)
            
        result['success'] = True
        result['data'] = result_list
        return result
        
    def bookReservation(self, reservation_data):
        url = self.base_url + '/reservations/'
        response = requests.post(url, headers = self.headers, json = reservation_data)
        result = {
            'success': False,
            'data': ''
        }
        if response.status_code != requests.codes.created:
            result['data'] = json.dumps(response.json())
            return result
        
        result['success'] = True
        return result

    def getBookingPoll(self, search_id):
        url = self.base_url + '/reservations/' + search_id + '/poll/'
        response = requests.get(url, headers = self.headers)
        result = {
            'success': False,
            'data': ''
        }
        if (response.status_code != requests.codes.accepted and
            response.status_code != requests.codes.ok):
            result['data'] = json.dumps(response.json())
            return result

        response = response.json()
        if (response['status'] == 'completed'):
            result['success'] = True
            result['data'] = response['reservations']
            return result

        if (response['status'] == 'pending'):
            time.sleep(2)
            return self.getBookingPoll(search_id)

        if (response['status'] == 'failed'):
            print('Booking failed! Search id: ' + search_id)
            result['data'] = json.dumps(response.json())
            return result
       
    def cancelBooking(self, reservation_id):
        url = self.base_url + '/reservations/' + reservation_id + '/'
        response = requests.delete(url, headers = self.headers)
        result = {
            'success': False,
            'data': ''
        }
        if response.status_code != requests.codes.accepted:
            result['data'] = json.dumps(response.json())
            return result
        
        result['success'] = True
        return result
