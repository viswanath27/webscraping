from docquery import document, pipeline
p = pipeline('document-question-answering')
doc = document.load_document("/Users/mspraja/Form_Linking/results/test/invoice_pwd.jpeg")
for q in ["What is the bill to?", "What is the invoice date?"]:
    print(q, p(question=q, **doc.context))