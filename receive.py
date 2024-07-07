import pika
import json
import requests

def search_icd10_code(chief_complaint):
    base_url = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"
    query_params = {
        "sf": "code,name",
        "terms": chief_complaint,
    }

    try:
        response = requests.get(base_url, params=query_params)
        response.raise_for_status()

        data = response.json()

        if data and data[1]:
            icd10_code = data[1][0]  # Retrieve the first ICD-10 code from the result
            return icd10_code

        print(f" [x] No result found for '{chief_complaint}'")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def callback(ch, method, properties, body):
    data = json.loads(body)
    chief_complaint = data.get('chief_complaint', '')
    
    # Search for ICD-10 code using the API
    icd10_code = search_icd10_code(chief_complaint)

    if icd10_code:
        print(f" [x] Received Chief Complaint: {chief_complaint}")
        print(f" [x] Corresponding ICD-10 Code: {icd10_code}")
    else:
        print(f" [x] Failed to retrieve the ICD-10 code for '{chief_complaint}'")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='chief_complaints_queue')

    channel.basic_consume(queue='chief_complaints_queue',
                          on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for Chief Complaints. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
