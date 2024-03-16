import csv
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape


# Define the path to your CSV file
csv_file_path = "data_invoice_ex.csv"

# Initialize a dictionaryto store the invoice data
invoice_data = {
    "meta": {},  # invoice_date, letterhead_text
    "payload": {
        "iss": {},  # name, address, city, state, zip, phone, email
        "aud": {},  # name, address, city, state, zip, phone, email,
        "sub": {},  # name, address, city, state, zip, phone, email
    },
}

# Read the CSV File, filtering empty cells

with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row = [cell for cell in row if cell]  # Remove empty cells
        # Check if the row contains project details, if not, it's part of the invoice detail
        if row[0] == "meta":
            key = row[1]
            invoice_data["meta"][key] = row[2:] if len(row) > 3 else row[2]
        else:  # payload
            key = row[1]
            claim_key = row[2]
            value = row[3:] if len(row) > 4 else row[3]
            invoice_data["payload"][key][claim_key] = value

# convert "invoice_date" (mm/dd/yyyy) to datetime object
invoice_data["meta"]["invoice_date"] = datetime.strptime(
    invoice_data["meta"]["invoice_date"], "%m/%d/%Y"
)

env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html"])
)
invoice_template = env.get_template("invoice.html")

# Render the invoice template with the invoice data
rendered_invoice = invoice_template.render(invoice_data=invoice_data)

# Save the rendered invoice to a file
with open("invoice.html", "w") as invoice_file:
    invoice_file.write(rendered_invoice)
    print("Invoice has been generated and saved as invoice.html")
