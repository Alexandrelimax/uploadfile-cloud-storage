from flask import Flask, request, jsonify
from google.cloud import storage, bigquery
from dotenv import load_dotenv
import os
load_dotenv()
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")
TABLE = os.environ.get("TABLE")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_account.json'

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

@app.route('/query', methods=['GET'])
def query_bigquery():
    client = bigquery.Client()
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE}`
        LIMIT 1000
    """
    data = client.query(query)
    results = data.result()

    results_list = [
        {"id": row["id"], "nome": row["nome"], "idade": row["idade"]}
        for row in results
    ]

    return jsonify(results_list)

@app.route('/insert', methods=['POST'])
def insert_data_into_bigquery():
    try:
        client = bigquery.Client()
        user_data = request.json

        table_ref = client.dataset(DATASET_ID).table(TABLE)
        table = client.get_table(table_ref)
        client.insert_rows(table, [user_data])

        return jsonify({"success": True, "message": "Os registros foram inseridos na tabela com sucesso."})


    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

