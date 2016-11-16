import textract
text = textract.process('/var/www/RTP/static/Report.docx')
print text
