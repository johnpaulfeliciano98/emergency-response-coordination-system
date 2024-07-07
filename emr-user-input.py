from datetime import datetime
import pika
import json


class PatientInformationSystem:
    def __init__(self):
        self.user_data = []
        self.rabbitmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.rabbitmq_connection.channel()
        self.channel.queue_declare(queue='chief_complaints_queue')

    def send_chief_complaint_to_rabbitmq(self, chief_complaint):
        """
        Sends chief complaint via RabbitMQ Pipe Spike
        """
        message = {'chief_complaint': chief_complaint}
        self.channel.basic_publish(
            exchange='',
            routing_key='chief_complaints_queue',
            body=json.dumps(message)
        )
        print(f"Chief complaint '{chief_complaint}' sent to RabbitMQ")

    def calculate_age(self, dob):
        today = datetime.now()
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        age = today.year - birth_date.year - \
            ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def get_user_input(self):
        name = input("Enter Full Name: ")
        dob, age = self.get_valid_dob()

        chief_complaints = input("Enter Chief Complaints: ")
        self.send_chief_complaint_to_rabbitmq(chief_complaints)
        hr = self.get_valid_integer("Enter Heart Rate (bpm): ")
        bp = self.get_valid_bp("Enter Blood Pressure (systolic/diastolic): ")
        rr = self.get_valid_integer("Enter Respiratory Rate (breaths/min): ")
        o2_saturation = self.get_valid_integer("Enter O2 Saturation (%): ")
        temperature = self.get_valid_float("Enter Temperature (Fahrenheit): ")
        eta = self.get_valid_integer("Enter ETA (minutes): ")
        los_options = ["BLS", "ALS", "CCT"]
        los = self.get_valid_los(los_options)

        user_info = {
            "name": name,
            "dob": dob,
            "age": age,
            "chief_complaints": chief_complaints,
            "vitals": {
                "hr": hr,
                "bp": bp,
                "rr": rr,
                "o2_saturation": o2_saturation,
                "temperature": temperature,
            },
            "eta": eta,
            "los": los.upper()
        }

        while True:
            self.display_user_information(user_info)
            edit_option = input(
                "\nEnter the number of the field you want to edit (1-6, 0 to submit, -1 to cancel): ")

            if edit_option == '0':
                print("\nPatient information has been sent to the hospital.")
                self.user_data.append(user_info)
                break
            elif edit_option == '-1':
                print("\nInput canceled. Exiting...\n")
                exit()
            elif 1 <= int(edit_option) <= 6:
                user_info = self.handle_edit_option(
                    int(edit_option), user_info, los_options)

    def handle_edit_option(self, option, user_info, los_options):
        if option == 1:
            user_info['name'] = input("Enter Full Name: ")
        elif option == 2:
            new_dob, new_age = self.get_valid_dob()
            user_info['dob'] = new_dob
            user_info['age'] = new_age
        elif option == 3:
            user_info['chief_complaints'] = input("Enter Chief Complaints: ")
        elif option == 4:
            vitals_edit_option = self.get_valid_vitals_edit_option()
            self.handle_vitals_edit(user_info, vitals_edit_option)
        elif option == 5:
            user_info['eta'] = self.get_valid_integer("Enter ETA (minutes): ")
        elif option == 6:
            user_info['los'] = self.get_valid_los(los_options)

        return user_info

    def handle_vitals_edit(self, user_info, vitals_edit_option):
        if vitals_edit_option in ['a', 'b', 'c', 'd', 'e']:
            vital_key = {'a': 'hr', 'b': 'bp', 'c': 'rr',
                         'd': 'o2_saturation', 'e': 'temperature'}[vitals_edit_option]
            user_info['vitals'][vital_key] = self.get_valid_vital_input(
                vital_key)

    def get_valid_vital_input(self, vital_key):
        prompt = f"Enter {self.get_vital_label(vital_key)}: "
        if vital_key == 'bp':
            return self.get_valid_bp(prompt)
        elif vital_key == 'temperature':
            return self.get_valid_float(prompt)
        else:
            return self.get_valid_integer(prompt)

    def get_vital_label(self, vital_key):
        vital_labels = {'hr': 'Heart Rate (bpm)', 'bp': 'Blood Pressure (systolic/diastolic)',
                        'rr': 'Respiratory Rate (breaths/min)', 'o2_saturation': 'O2 Saturation (%)',
                        'temperature': 'Temperature (Fahrenheit)'}
        return vital_labels[vital_key]

    def get_valid_dob(self):
        while True:
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")
            try:
                datetime.strptime(dob, "%Y-%m-%d")
                age = self.calculate_age(dob)
                return dob, age
            except ValueError:
                print(
                    "Invalid date format. Please enter Date of Birth in the format YYYY-MM-DD.")

    def get_valid_integer(self, prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def get_valid_bp(self, prompt):
        while True:
            bp_input = input(prompt)
            bp_parts = bp_input.split('/')
            if len(bp_parts) == 2 and all(part.isdigit() for part in bp_parts):
                return bp_input
            else:
                print(
                    "Invalid input format. Please enter Blood Pressure in the format 'int/int'.")

    def get_valid_float(self, prompt):
        while True:
            try:
                value = float(input(prompt) or '0')
                return value
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_valid_los(self, los_options):
        while True:
            los = input(f"Enter Level of Service (Choose from {
                        ', '.join(los_options)}): ")
            if los.upper() in los_options:
                return los.upper()
            else:
                print(
                    "Invalid input. Please enter a valid Level of Service (BLS, ALS, CCT).")

    def get_valid_vitals_edit_option(self):
        while True:
            print("\nVitals Edit Options:")
            print("a. Heart Rate (bpm)")
            print("b. Blood Pressure (systolic/diastolic)")
            print("c. Respiratory Rate (breaths/min)")
            print("d. O2 Saturation (%)")
            print("e. Temperature (Fahrenheit)")
            print("0. Submit")
            print("-1. Cancel")

            vitals_edit_option = input(
                "\nEnter the letter of the vitals field you want to edit (a-e, 0 to submit, -1 to cancel): ")

            if vitals_edit_option in ['a', 'b', 'c', 'd', 'e', '0', '-1']:
                return vitals_edit_option
            else:
                print("\nInvalid option. Please enter a valid letter or number.")

    def display_user_information(self, user_info):
        print("\nEntered Information:")
        print("1. Name:", user_info['name'])
        print("2. Date of Birth:", user_info['dob'])
        print("   Age:", user_info['age'])
        print("3. Chief Complaints:", user_info['chief_complaints'])
        print("4. Vitals:")
        for key, value in user_info['vitals'].items():
            print(f"   {self.get_vital_label(key)}: {value}")
        print("5. ETA:", user_info['eta'], "minutes")
        print("6. Level of Service (LOS):", user_info['los'])


if __name__ == "__main__":
    patient_system = PatientInformationSystem()
    patient_system.get_user_input()