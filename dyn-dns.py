import requests
import datetime
import time
import os

# File to store the previous IP address
IP_FILE = 'previous_ip.txt'

def get_current_ip():
    """Retrieve the current public IP."""
    try:
        response = requests.get("https://ipinfo.io")
        response.raise_for_status()
        data = response.json()
        return data.get("ip")
    except requests.RequestException as e:
        print(f"Error retrieving current IP: {e}")
        return None

def get_previous_ip():
    """Read the previous IP address from the file."""
    if os.path.exists(IP_FILE):
        with open(IP_FILE, 'r') as file:
            return file.read().strip()
    return None

def save_current_ip(ip):
    """Save the current IP address to the file."""
    with open(IP_FILE, 'w') as file:
        file.write(ip)

def update_dns_record(new_ip):
    """Update DNS record using curl."""
    username = "your_username"
    password = "your_password"
    hostname = "mytest.example.com"
    
    headers = {
        "User-Agent": "Company DeviceName-Model/FirmwareVersionNumber maintainer-contact@example.com"
    }
    
    url = f"https://dynupdate.no-ip.com/nic/update?hostname={hostname}&myip={new_ip}"
    response = requests.get(url, headers=headers, auth=(username, password))
    return response.text.strip()

while True:
    # Get the current public IP
    current_ip = get_current_ip()
    
    if current_ip is None:
        print("Could not retrieve current IP. Skipping this iteration.")
        time.sleep(3600)
        continue

    # Print timestamp
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time}")
    
    # Get the previous IP from the file
    previous_ip = get_previous_ip()

    # Compare current IP with the previous IP
    if previous_ip is None:
        print("No previous IP found. This is the first run or the file was deleted.")
        print("Current IP:", current_ip)
        save_current_ip(current_ip)
    else:
        if current_ip != previous_ip:
            print("IP has changed!")
            print("Previous IP:", previous_ip)
            print("Current IP:", current_ip)
            
            # Update DNS record
            response = update_dns_record(current_ip)
            print("DNS Update Response:", response)
            
            # Save the new IP
            save_current_ip(current_ip)
        else:
            print("IP has not changed.")
    
    # Sleep for 60 minutes
    time.sleep(3600)
