import requests
import csv

# Replace with your valid access token
access_token = "Apbq6RpweFHpP6GXzqkUiECmLsXS"

# Amadeus API endpoint for flight offers
base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# Query parameters for the API request
query_params = {
    "originLocationCode": "TUN",
    "destinationLocationCode": "CDG",
    "departureDate": "2024-12-25",
    "adults": 1,
    "nonStop": "false",
    "max": 250
}

# Headers with the Bearer token for authorization
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Send GET request to Amadeus API
response = requests.get(base_url, headers=headers, params=query_params)

if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()

        # Open a CSV file to save the flight offers
        with open("flight_offers.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(["Departure", "Arrival", "Price", "Departure Date", "Arrival Date"])

            # Extract flight offers from the response
            for offer in data.get('data', []):
                # Extract details of the first segment
                departure_airport = offer['itineraries'][0]['segments'][0]['departure']['iataCode']
                arrival_airport = offer['itineraries'][0]['segments'][0]['arrival']['iataCode']
                departure_date = offer['itineraries'][0]['segments'][0]['departure']['at']
                arrival_date = offer['itineraries'][0]['segments'][0]['arrival']['at']
                price = offer['price']['total']

                # Print flight details
                print(f"Departure: {departure_airport}")
                print(f"Arrival: {arrival_airport}")
                print(f"Price: {price}")
                print(f"Departure Date: {departure_date}")
                print(f"Arrival Date: {arrival_date}")
                print("--------------------")

                # Write flight details to the CSV file
                writer.writerow([departure_airport, arrival_airport, price, departure_date, arrival_date])

        print("Flight offers have been saved to flight_offers.csv")

    except KeyError as e:
        print(f"Missing key in response: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print(f"Error fetching flight offers (HTTP {response.status_code}):", response.text)