import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image

# Define the path for the blank icon
icon_path = 'C:\\Users\\Frank\\Desktop\\blank.ico'

# Create a function to generate a blank icon
def create_blank_ico(path):
    size = (16, 16)
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    image.save(path, format="ICO")

# Create the blank ICO file
create_blank_ico(icon_path)

# API Configuration
API_KEY = 'API Key Here'  # Replace with your actual Fixer.io API key
BASE_URL = 'http://data.fixer.io/api'

# Function to get exchange rates
def get_exchange_rates():
    url = f'{BASE_URL}/latest?access_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['success']:
        rates = data['rates']
        # Ensure EUR is included in the rates
        if 'EUR' not in rates:
            rates['EUR'] = 1.0
        return rates, data['date']
    else:
        raise Exception('Error fetching exchange rates.')

# Fetch exchange rates at the start
try:
    exchange_rates, last_updated = get_exchange_rates()
except Exception as e:
    print("Error fetching exchange rates:", e)
    exchange_rates = None
    last_updated = 'Unknown'

# Limit the currencies to EUR, GBP, USD, AUD, JPY, and ZAR
available_currencies = ['EUR', 'GBP', 'USD', 'AUD', 'JPY', 'ZAR', 'CNY']

def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_combobox.get()
        to_currency = to_currency_combobox.get()

        if exchange_rates is None:
            raise Exception('Exchange rates data is not available.')

        if from_currency not in exchange_rates:
            raise Exception(f"Currency {from_currency} not available.")
        if to_currency not in exchange_rates:
            raise Exception(f"Currency {to_currency} not available.")

        rate_from = exchange_rates[from_currency]
        rate_to = exchange_rates[to_currency]

        rate = rate_to / rate_from
        converted_amount = amount * rate

        # Cross rate is rate
        cross_rate = rate

        # Reverse cross rate is 1 / rate
        reverse_cross_rate = 1 / rate

        # Display the result and both cross rates
        result_label.config(text=f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
        cross_rate_label.config(text=f"Cross Rate: 1 {from_currency} = {cross_rate:.4f} {to_currency} \n"
                                     f"Reverse Rate: 1 {to_currency} = {reverse_cross_rate:.4f} {from_currency}")

        # Update the last updated label
        last_updated_label.config(text=f"Rates last updated on: {last_updated}")
    except Exception as e:
        result_label.config(text="Error in conversion. Please check inputs.")
        cross_rate_label.config(text="")
        last_updated_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Currency Conv")

# Set custom icon
root.iconbitmap(icon_path)

# Create and place the widgets
amount_label = tk.Label(root, text="Enter amount:")
amount_label.grid(row=0, column=0, padx=10, pady=10)

amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

from_currency_label = tk.Label(root, text="From currency:")
from_currency_label.grid(row=1, column=0, padx=10, pady=10)

from_currency_combobox = ttk.Combobox(root, values=available_currencies, state="readonly")
from_currency_combobox.grid(row=1, column=1, padx=10, pady=10)
from_currency_combobox.set('USD')  # Set a default value

to_currency_label = tk.Label(root, text="To currency:")
to_currency_label.grid(row=2, column=0, padx=10, pady=10)

to_currency_combobox = ttk.Combobox(root, values=available_currencies, state="readonly")
to_currency_combobox.grid(row=2, column=1, padx=10, pady=10)
to_currency_combobox.set('EUR')  # Set a default value

convert_button = tk.Button(root, text="Convert", command=convert_currency, bg="#d0e8f1", font=("Helvetica", 8))
convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Label to display the conversion result
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Label to display the cross rate
cross_rate_label = tk.Label(root, text="")
cross_rate_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Label to display the last updated date
last_updated_label = tk.Label(root, text="")
last_updated_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the main loop
root.mainloop()
