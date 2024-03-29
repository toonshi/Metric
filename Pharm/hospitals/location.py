import os
import requests
from django.conf import settings
from hospitals.models import Institution  # Assuming Institution is your model

def run_script():
    base_country = settings.BASE_COUNTRY
    api_key = settings.GOOGLE_API_KEY
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    
def fetch_hospitals(base_country):
    api_key = settings.GOOGLE_API_KEY
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    
    params = {
        'query': f'hospitals in {base_country}',
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'results' in data:
        hospitals = data['results']
        for hospital in hospitals:
            name = hospital['name']
            country = base_country
            latitude = hospital['geometry']['location']['lat']
            longitude = hospital['geometry']['location']['lng']
            address_components = hospital.get('address_components', [])
            county = next((comp['long_name'] for comp in address_components if 'administrative_area_level_2' in comp['types']), None)
            postal_code = next((comp['long_name'] for comp in address_components if 'postal_code' in comp['types']), None)
            
            # Create or update Institution instance
            institution, created = Institution.objects.update_or_create(
                name=name,
                country=country,
                latitude=latitude,
                longitude=longitude,
                county=county,
                postal_code=postal_code
            )
            
            print(f'{"Created" if created else "Updated"} institution: {institution.name}')
    else:
        print('No hospitals found.')

if __name__ == '__main__':
    base_country = settings.BASE_COUNTRY  # Use base country from settings
    fetch_hospitals(base_country)
