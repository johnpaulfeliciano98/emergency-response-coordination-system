# EMR User Input and ICD-10 Processor Microservices

This microservice allows users to submit patient information, including chief complaints, to receive corresponding ICD-10 codes.

The communication between the sender (EMR User Input) and the receiver (ICD-10 Processor) is established using RabbitMQ.

## Prerequisites

1. **RabbitMQ** : Install RabbitMQ. You can download it from [RabbitMQ official website]().
2. **Python Libraries** : Install the required Python libraries using the following command: pip install pika requests

## Communication Contract

### Sending Data (EMR User Input)

#### Request

* Endpoint: RabbitMQ Queue - `chief_complaints_queue`
* Payload: JSON object containing user information

  {
  "name":"John Doe",
  "dob":"1990-01-01",
  "age":32,
  "gender":"M",
  "chief_complaints":"Chest pain",
  "vitals":{
  "hr":75,
  "bp":"120/80",
  "rr":18,
  "o2_saturation":98,
  "temperature":98.6
  },
  "eta":15,
  "los":"ALS"
  }

### Receiving Data (ICD-10 Microservice)

#### Response

* The ICD-10 microservice will print the received chief complaint and its corresponding ICD-10 code.

  [x]Received Chief Complaint: Chest pain
  [x]Corresponding ICD-10 Code: I20.9

## Example Call

1. **Send Patient Information from EMR User Input**
   * Run `emr-user-input.py`
   * Enter patient information as prompted.
   * After entering all details, choose option `0` to submit.
   * The patient information, including chief complaint, will be sent to the microservice via RabbitMQ.
2. **Receive and Process in ICD-10 Processor**
   * Run `receive.py`
   * The microservice will consume messages from the RabbitMQ queue.
   * It will print the received chief complaint and its corresponding ICD-10 code.
