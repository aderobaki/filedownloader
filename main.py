import os
import requests
import csv
from urllib.parse import urlsplit
from pathlib import Path

# Function to download a file from a given URL
def download_file(url, dest_folder):
    try:
        # Get the filename from the URL
        filename = os.path.basename(urlsplit(url).path)
        if not filename:  # If the URL does not contain a file name, skip it
            print(f"Skipping URL without a file: {url}")
            return
        
        # Create the destination folder if it doesn't exist
        Path(dest_folder).mkdir(parents=True, exist_ok=True)

        # Define the full path for the file to be saved
        file_path = os.path.join(dest_folder, filename)

        # Send a GET request to the URL
        response = requests.get(url, stream=True)

        # If the response status code is OK (200), save the file
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url} with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

# Main function to read URLs from CSV and download files
def download_files_from_csv(csv_file_path, dest_folder):
    try:
        # Open the CSV file
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)

            # Iterate through each row in the CSV
            for row in csv_reader:
                if row:  # Check if the row is not empty
                    url = row[0]  # Assuming URL is in the first column
                    download_file(url, dest_folder)
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")

# Define the path to the CSV file and the destination folder
csv_file_path = 'urls.csv'  # Replace with the path to your CSV file
dest_folder = 'downloaded_files'  # Replace with your desired destination folder

# Run the function to download files
download_files_from_csv(csv_file_path, dest_folder)
