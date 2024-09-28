from PyPDF2 import PdfReader, PdfWriter
import os

# Ask the user for the input PDF file path
pdf_file_path = input("Enter the full path of the input PDF file: ")

# Check if the file exists
if not os.path.isfile(pdf_file_path):
    print("Error: The specified file does not exist.")
    exit()

# Ask the user for the output directory
output_dir = input("Enter the path of the output directory: ")

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Opens the original PDF
reader = PdfReader(pdf_file_path)

# Define split points (end pages for each part)
split_pnts = [286, 572, 853]  # Adjust these as necessary

# Splitting into parts
start_page = 0
for i, end_page in enumerate(split_pnts):
    writer = PdfWriter()
    
    # Insert pages into the new PDF
    for page in range(start_page, end_page):
        writer.add_page(reader.pages[page])
    
    # Create the output file name and save the PDF in the specified directory
    output_filename = os.path.join(output_dir, f"output_part_{i+1}.pdf")
    with open(output_filename, "wb") as output_pdf:
        writer.write(output_pdf)
    
    print(f"Part {i+1} saved as {output_filename}")

    # Update the start page for the next part
    start_page = end_page
