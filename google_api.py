import pandas as pd
import googlemaps
from locations import *


def google_api_call(api_key) :

  gmaps = googlemaps.Client(key=api_key)

  brand_dict = {'Genesis': genesis,'Hyundai': hyundai,'Hyundai - Al Majdouie': hyundai_majdouie,'Hyundai - Al Wallan' : hyundai_wallan,'Hyundai - Naghi' : hyundai_naghi,\
                'Changan': changan,'Peugeot & Citroen': citroen_peugeot,'Toyota': toyota,'Lexus': lexus,'Kia': kia,'Geely': geely,'Ford': ford,'Mazda': mazda,'GAC': GAC,\
                'GMC & Chevrolet': gmc_chevrolet,'Cadillac': cadillac,'Nissan': nissan,'MG': mg,'Mitsubishi':mitsubishi,'Mercedes': mercedes,'BMW':BMW,'Audi': audi,}

  columns = ['Brand', 'Name', 'City', 'Region', 'District', 'Rating', 'Review Count', 'Address', 'latitude', 'Longitude', 'PlaceID']
  df = pd.DataFrame(columns=columns)

  # Function to extract specific address component
  def get_address_component(components, component_type):
      for component in components:
          if component_type in component['types']:
              return component['long_name']
      return "Not found"

  # Function to get place details using Place ID
  def get_place_details(place_id):
      place_details = gmaps.place(place_id=place_id)
      name = place_details['result']['name']
      rating = place_details['result'].get('rating', None)
      review_count = place_details['result'].get('user_ratings_total', None)
      city = get_address_component(place_details['result']['address_components'], 'locality')
      region = get_address_component(place_details['result']['address_components'], 'administrative_area_level_1')
      district = get_address_component(place_details['result']['address_components'], 'administrative_area_level_2')
      address = place_details['result'].get('formatted_address', None)
      latitude = place_details['result']['geometry']['location']['lat']
      longitude = place_details['result']['geometry']['location']['lng']

      return name, city, region, district, rating, review_count, address, longitude, latitude

  for key, value in brand_dict.items():
      for item in value:
        name, city, region, district, rating, review_count, address, longitude, latitude = get_place_details(item)
        df.loc[len(df.index)] = [key, name, city, region, district, rating, review_count, address, latitude, longitude, item]

  return df