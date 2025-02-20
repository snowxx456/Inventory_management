import cv2
from pyzbar.pyzbar import decode
from picamera import PiCamera
from picamera.array import PiRGBArray
import requests
import base64
import json
import time
from datetime import datetime

# Replace with your actual access token
token = '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'
name_of_check_person = input("Enter Name of the Checking person : ")

# Set up authentication headers
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Function to get file contents from GitHub
def get_file_contents(repo_url):
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 200:
        content = response.json()
        return content
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Function to update file contents on GitHub
def update_file_content(update_url, new_content, existing_sha):
    encoded_content = base64.b64encode(new_content.encode()).decode()

    update_data = {
        "message": "Update file",
        "content": encoded_content,
        "sha": existing_sha
    }

    update_response = requests.put(update_url, headers=headers, data=json.dumps(update_data))

    if update_response.status_code == 200:
        print("File updated successfully!")
    else:
        print("Failed to update file:", update_response.status_code)

# Function to scan QR code and update a master dictionary
def scan_qr():
    # Initialize the PiCamera and grab a reference to the raw capture
    camera = PiCamera()
    raw_capture = PiRGBArray(camera)

    # Allow the camera to warm up
    camera.start_preview()

    master_qr_data = {}

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        # Decoding QR code
        decoded_objects = decode(image)
       
        for obj in decoded_objects:
            # Extracting data from QR code
            qr_data = obj.data.decode().split('\n')
            qr_dict = {}
            for data in qr_data:
                key, value = data.split(': ')
                qr_dict[key] = value

            # Checking if the data already exists in the master dictionary
            exists = False
            for key, value in master_qr_data.items():
                if value == qr_dict:
                    exists = True
                    break
           
            # If the data doesn't exist, add it to the master dictionary
            if not exists:
                key = f"QR_{len(master_qr_data) + 1}"
                master_qr_data[key] = qr_dict
                print(f"Added QR Data {key} to Master Dictionary:", qr_dict)
               
                # Print the current date and time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Scanning Time:", current_time)
                owner = 'dronelog-uasnmims'
                repo = 'qr-code'
                file_path = 'data.csv'

                # Construct the URL for file operations
                file_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'

                # Get current file content
                file_info = get_file_contents(file_url)

                if file_info:
                    existing_content = base64.b64decode(file_info['content']).decode()
                    existing_sha = file_info['sha']

                    # New content to be added
                    new_content = (f"\n{qr_dict['Bin']},{qr_dict['Location']},{qr_dict['Part No']},{qr_dict['Name']},{current_time},available,{name_of_check_person}")

                    # Update file content
                    update_file_content(file_url, existing_content + new_content, existing_sha)

        cv2.imshow('QR Scanner', image)
        raw_capture.truncate(0)
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.close()
    cv2.destroyAllWindows()

    return master_qr_data

# Call the function to start scanning
master_qr_data = scan_qr()
print("Master QR Data Dictionary:", master_qr_data)
