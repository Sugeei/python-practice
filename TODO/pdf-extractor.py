import camelot.camelot as camelot


# dependences: PyPDF2
# https://pypi.org/project/PyPDF2/#files
# https://pypi.org/project/pycryptodome/#files
# https://pypi.org/project/sortedcontainers/#files
# https://pypi.org/project/chardet/#files
# https://pypi.org/project/pdfminer.six/#files

tables = camelot.read_pdf('report1.pdf')

print(tables[0].df)

import ghostscript
