import tkinter as tk
from tkinter import ttk
from currency_converter import CurrencyConverter
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

# Create the CurrencyConverter object
c = CurrencyConverter()

# Limit the currencies to EUR, GBP, USD, AUD, JPY, and ZAR
available_currencies = ['EUR', 'GBP', 'USD', 'AUD', 'JPY', 'ZAR']

def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_combobox.get()
        to_currency = to_currency_combobox.get()

        # Perform the conversion
        converted_amount = c.convert(amount, from_currency, to_currency)
        
        # Get the cross rate (from -> to)
        cross_rate = c.convert(1, from_currency, to_currency)
        
        # Get the reverse cross rate (to -> from)
        reverse_cross_rate = c.convert(1, to_currency, from_currency)
        
        # Display the result and both cross rates
        result_label.config(text=f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
        cross_rate_label.config(text=f"Cross Rate: 1 {from_currency} = {cross_rate:.4f} {to_currency} \n"
                                     f"Reverse Rate: 1 {to_currency} = {reverse_cross_rate:.4f} {from_currency}")
        
        # Call the show_last_updated function to display the update info
        show_last_updated()
    except Exception as e:
        result_label.config(text="Error in conversion. Please check inputs.")
        cross_rate_label.config(text="")

def show_last_updated():
    try:
        # Get the last available date from the CurrencyConverter's data
        last_updated = max(c._rates['USD'].keys())  # or any other available currency like 'EUR'
        
        # Display the last updated date in a label
        last_updated_label.config(text=f"Rates last updated on: {last_updated}")
    except Exception as e:
        last_updated_label.config(text="Cannot retrieve update date.")

# Create the main window
root = tk.Tk()
root.title("Currency Convert")

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

# Label to display the last updated date (this will be updated when the Convert button is pressed)
last_updated_label = tk.Label(root, text="")
last_updated_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the main loop
root.mainloop()
