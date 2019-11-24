import camelot

# https://bigdata-s3.wmcloud.com/researchreport/cc/e26a08d2f0d6d651d1b8c3aa4480f491.pdf

tables = camelot.read_pdf('e26a08d2f0d6d651d1b8c3aa4480f491.pdf')
print(tables[0].df)

# https://github.com/atlanhq/camelot/issues/282
# https://www.ghostscript.com/download/gsdnld.html
# cannot download ghostscript......