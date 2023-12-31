import requests
import datetime
import time

# Initialize last known public IP
last_ip = None

# Function to retrieve the current public IP
def get_current_ip():
    response = requests.get("https://ipinfo.io")
    data = response.json()
    return data.get("ip")

# Update DNS record using curl
def update_dns_record(new_ip):
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

    # Print Timestamp action
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time}")

    # Compare current IP with the last known IP
    if last_ip is None:
        last_ip = current_ip
        print("Initial IP:", last_ip)
    else:
        if current_ip != last_ip:
            print("IP has changed!")
            print("Previous IP:", last_ip)
            print("Current IP:", current_ip)
            
            # Update DNS record
            response = update_dns_record(current_ip)
            print("DNS Update Response:", response)
            
            last_ip = current_ip
        else:
            print("IP has not changed.")

    # Sleep for 60 minutes
    time.sleep(3600)
