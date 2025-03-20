# Automated ICD-10 Coding for EMR Data

This project implements two microservices designed to streamline patient data processing:

- **EMR User Input Microservice:** Collects patient details (including chief complaints) and sends the data via RabbitMQ.
- **ICD-10 Processor Microservice:** Consumes messages from RabbitMQ, processes the chief complaint, and outputs the corresponding ICD-10 code.

The services communicate asynchronously using RabbitMQ, ensuring reliable and decoupled integration.

## Prerequisites

Before running the microservices, make sure you have the following installed:

- **RabbitMQ:**  
  Download and install RabbitMQ from the [official website](https://www.rabbitmq.com/).

- **Python Libraries:**  
  Install the required Python packages using pip:
  ```bash
  pip install pika requests
  ```

## Communication Contract

### 1. Sending Data from EMR User Input

- **Queue Name:** `chief_complaints_queue`
- **Payload Format:** JSON object containing patient information.

**Example Payload:**

```json
{
    "name": "John Doe",
    "dob": "1990-01-01",
    "age": 32,
    "gender": "M",
    "chief_complaints": "Chest pain",
    "vitals": {
        "hr": 75,
        "bp": "120/80",
        "rr": 18,
        "o2_saturation": 98,
        "temperature": 98.6
    },
    "eta": 15,
    "los": "ALS"
}
```

### 2. Receiving Data in ICD-10 Processor

Upon receiving a message, the ICD-10 Processor microservice will:

- Parse the chief complaint.
- Determine the corresponding ICD-10 code.
- Print both the chief complaint and the ICD-10 code to the console.

**Example Output:**

```plaintext
[x] Received Chief Complaint: Chest pain
[x] Corresponding ICD-10 Code: I20.9
```

## Running the Microservices

### EMR User Input Microservice

- **File:** `emr-user-input.py`

**Instructions:**

1. Run the script:

    ```bash
    python emr-user-input.py
    ```

2. Follow the prompts to enter patient information.
3. When finished, choose option `0` to submit. The patient information is then sent to RabbitMQ.

### ICD-10 Processor Microservice

- **File:** `receive.py`

**Instructions:**

1. Run the script:

    ```bash
    python receive.py
    ```

2. The microservice will listen to the `chief_complaints_queue`, process incoming messages, and display the results.

## Additional Information

### Message Flow

- The EMR User Input service acts as the **producer** (sending patient data), while the ICD-10 Processor service acts as the **consumer** (receiving and processing the data).

### Customization

- Both microservices can be extended or integrated with additional services as needed.

## Troubleshooting

### RabbitMQ Connection

- Ensure that RabbitMQ is running on `localhost` and the queue `chief_complaints_queue` is properly declared.

### Input Validation

- The `emr-user-input.py` script includes input validation. If you encounter errors, follow the on-screen prompts to correct the input format.
