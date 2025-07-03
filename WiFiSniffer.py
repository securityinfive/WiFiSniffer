# A Simple WiFi Scanner. This will scan for all detectable WiFi networks in range on the PC. 
# It will capture the name, SID, signal strength, frequenciy and security)
# You can expand this to store in a SQLite DB and record and trend over time. 
# Add detected data and maybe add the network you are currently connected to 
# If you are mobile with a laptop. 

# pywifi kept throwing unrecognized error although it was installed, added the ignore, works fine.
# Note - when you pip install pywifi and run it, you may get can't find comtypes. Pip install comtypes seperate.
import pywifi # type: ignore
from pywifi import const  # type: ignore
import time
import csv
import datetime


# Initialize WiFi interface
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]  # Get the first WiFi adapter

# Start scanning
print("🔍 Scanning for available WiFi networks... (waiting 10 seconds)")

iface.scan()
time.sleep(10)  # Allow time for the scan to complete, if zero results, extend sleep

# Get scan results
results = iface.scan_results()

# Remove duplicates based on SSID + BSSID
unique_networks = {}
for network in results:
    key = (network.ssid, network.bssid)
    if key not in unique_networks:
        unique_networks[key] = network

# CSV output path with timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"wifi_scan_{timestamp}.csv"

# Write to CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["SSID", "BSSID", "Signal Strength (dBm)", "Frequency (MHz)", "Security"])

    print(f"\n{'SSID':<35}", end=" ")
    print(f"{'BSSID':<20}", end=" ")
    print(f"{'Signal':<7}", end=" ")
    print(f"{'Freq.':<12}")
    print(f"{'----------':<35}", end=" ")
    print(f"{'----------':<20}", end=" ")
    print(f"{'------':<7}", end=" ")
    print(f"{'----------':<12}")
    for network in unique_networks.values():
        ssid = network.ssid
        print(f"{ssid:<35}", end=" ")
        bssid = network.bssid
        print(f"{bssid:<20}", end=" ")
        signal = network.signal  # Typically negative; closer to 0 is better
        print(f"{signal:<7}", end=" ")
        freq = network.freq
        print(f"{freq:<9}")
        auth = network.akm if network.akm else ["OPEN"]
        auth_str = ', '.join(str(a) for a in auth)
        writer.writerow([ssid, bssid, signal, freq, auth_str])
        
        # Can clean up the print to print in a grid, evenly spaced later
        # print(ssid, bssid, signal, auth_str)
        

print(f"\n✅ Scan complete. Results saved to: {csv_filename}")

