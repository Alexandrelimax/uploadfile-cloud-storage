from flask import Flask, request, jsonify
from google.cloud import storage
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'conseguimos'})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        client = storage.Client()
        bucket = client.get_bucket('bucket_alexandre_teste')
        blob = bucket.blob(file.filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)
        return jsonify('File uploaded successfully')


@app.route('/download', methods=['GET'])
def download_file():

    client = storage.Client()
    bucket = client.get_bucket('bucket_alexandre_teste')
    blob = bucket.blob('714155.jpg')
    with open(os.path.join(os.getcwd(), 'downloads_files', '714155.jpg'), 'wb') as file:
        client.download_blob_to_file(blob, file)

    return jsonify('File downloaded successfully')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
