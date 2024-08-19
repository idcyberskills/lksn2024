import os
import requests
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
from xhtml2pdf import pisa 
from io import BytesIO
import helpers

app = Flask(__name__)
PORT=7755

def add_paragraph(text, content):
    """ Add paragraph to document content"""
    content.append(Paragraph(text))

def get_document_template(stream_file: BytesIO):
    """ Get SimpleDocTemplate """
    return SimpleDocTemplate(stream_file)

def build_document(document, content, **props):
    """ Build pdf document based on elements added in `content`"""
    document.build(content, **props)

@app.route('/create', methods=['POST'])
def submit_urls():
    data = request.get_json()
    urls = data.get('urls', [])

    processed_urls = []
    for i, u in enumerate(urls):
        res = requests.get(u)
        
        if res.status_code == 200:
            content_type = res.headers.get('Content-Type', '')
            if 'text/html' in content_type:
                title = helpers.get_page_title(res.content)
                u = helpers.extract_image_url(res.content)
            elif content_type.startswith('image/'):
                title = f"Image {i}"
        
        processed_urls.append({'url': u, 'title': title})
    
    print(processed_urls)
    html = render_template('window.html', urls=processed_urls)
    print(html)

    pdf_filename = f"my_portfolio_{helpers.generate_random_string()}.pdf"
    pdf_path = os.path.join('pdfs', pdf_filename)
    result_file = open(pdf_path, 'wb')
    pisa_status = pisa.CreatePDF(html.encode("utf-8"), dest=result_file, show_error_as_pdf=True, encoding='UTF-8') 
    result_file.close()
    
    # Process the URLs as needed
    # For demonstration, we'll just return the received URLs
    print("Received URLs:", urls)
    
    return jsonify({"status": "success", "urls": urls})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render():
    data = request.get_json()
    urls = data.get('urls', [])

    processed_urls = []
    for u in urls:
        res = requests.get(u)
        if res.status_code == 200:
            title = helpers.get_page_title(res.content)
        
        processed_urls.append({'url': u, 'title': title})
    
    return render_template('window.html', urls=processed_urls)
    

if __name__ == '__main__':
    app.run(debug=True, port=PORT)