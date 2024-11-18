import requests

def get_currency_map():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url).json()
    currency_map = {}
    
    for country_data in response:
        if 'currencies' in country_data:
            country = country_data['name']['common']
            currency = list(country_data['currencies'].keys())[0]
            currency_map[country] = currency
    return currency_map

def convert_currency(currency_map):
    print("RATE MASTER")
    print("______________")
    while True:
        amount = input("Amount: ")
        if amount == '0':
            print("Thank you for using the currency converter.")
            break
        
        try:
            amount = float(amount)
        except ValueError:
            print('Invalid input.Enter a  number.')
            continue
        
        from_country = input("From Country: ")
        to_country = input("To Country: ")
        
        from_currency = currency_map.get(from_country)
        to_currency = currency_map.get(to_country)
        
        if not from_currency or not to_currency:
            print("Country or currency not found.")
            continue
        
        try:
            url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            rate = data['rates'].get(to_currency)
            if rate:
                converted_amount = amount * rate
                print(f"RESULT: {amount} {from_country} ({from_currency}) = {converted_amount:.2f} {to_country} ({to_currency})")
            else:
                print("Rate not available.")
        except:
            print("Error getting rate")
            
def main():
    currency_map = get_currency_map()
    if currency_map:
        convert_currency(currency_map)

main()