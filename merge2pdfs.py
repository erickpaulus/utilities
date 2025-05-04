# Please make sure you already have these libraries 
# pip install PyPDF2 

from PyPDF2 import PdfMerger

# Create a PdfMerger object
merger = PdfMerger()

# List of PDF files to merge
pdfs = [rf"C:\Users\ErickP\Downloads\IEEE young Professionals.pdf", rf'C:\Users\ErickP\Downloads\Membership and Subscription Information IEEE.pdf']

# Append each file
for pdf in pdfs:
    merger.append(pdf)

# Write out the merged PDF
merger.write('IEEE young Professionals merged.pdf')
merger.close()

print("PDFs merged successfully into 'merged.pdf'")
