# QR Code Repository

This repository contains scripts and files to manage QR code data for an inspecting drone.

## Files

- **drone_log_ground_station.py**: Python script responsible for interacting with the GitHub API to process QR code data.
- **qr_raspberrypi.py**: Script designed to run on a Raspberry Pi with a camera module. Scans QR codes and updates data on GitHub.
- **index.html**: HTML file displaying data from the `local_data.csv` file, updated by `drone_log_ground_station.py`.
- **unavailable.py**: Updates the `local_data.csv` file to display unavailable data.

## Usage

### Setup

1. Clone the repository locally.
2. Ensure required libraries are installed (for Python scripts).
3. Customize access tokens and repository details in the scripts:
    - `drone_log_ground_station.py`: Update `owner`, `repo`, `file_path`, and `token` with your repository information and access token.
    - `qr_raspberrypi.py`: Set the `token` variable with your access token.

### Running the Scripts

- **drone_log_ground_station.py**:
  - Execute this script to manage data fetched from the inspecting drone.
- **qr_raspberrypi.py**:
  - Run this script on a Raspberry Pi with a camera module. It scans QR codes and updates data on GitHub.

### HTML Display

- Open `index.html` in a web browser to view a dynamically updated table of data from `local_data.csv`.

### Logo

- `uasnmims_LITT.jpeg` is the logo of our team, 🔥LITT🔥 at NMIMS Shirpur.

### Important Notes

- Ensure permissions and access rights are correctly set for GitHub repositories when using access tokens.
- Modifications to the scripts should be made carefully to avoid unintended changes to the data.


