import requests

def fetch_country_currency_mapping():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url).json()
    country_currency_mapping = {}
    for country in response:
        if 'currencies' in country:
            country_name = country['name']['common']
            currency_code = list(country['currencies'].keys())[0]
            country_currency_mapping[country_name] = currency_code
    return country_currency_mapping

def convert_currency_by_country(country_currency_map):
    while True:
        print("CURRENCY CONVERTER")
        print("_______________________")
        amount_input = input('AMOUNT: ')
        
        if not amount_input.replace('.', '', 1).isdigit():
            print("Invalid amount. Please enter a number without letters.")
            continue
        
        try:
            amount = float(amount_input)
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            continue
        
        from_country = input('FROM COUNTRY: ')
        to_country = input('TO COUNTRY: ')
  
        from_currency = country_currency_map.get(from_country)
        to_currency = country_currency_map.get(to_country)
        
        if not from_currency or not to_currency:
            print("Invalid country names or no currency found.")
            continue

        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            
            rate = data['rates'].get(to_currency)
            if rate:
                converted_amount = amount * rate
                print("RESULT: ", f"{amount} {from_country} ({from_currency}) = {converted_amount:.2f} {to_country} ({to_currency})")
            else:
                print("Conversion rate not available.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching conversion rate: {e}")
            choice = input("USE CURRENCY CONVERTER AGAIN?")
            if choice == "YES" or choice == "yes":pass
            else:
                break
            
if __name__ == "__main__":
    country_currency_map = fetch_country_currency_mapping()
    if country_currency_map:
        convert_currency_by_country(country_currency_map)
    else:
        print("Could not retrieve country data.")