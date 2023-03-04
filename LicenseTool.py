import base64
import subprocess
import os

def encode(serial, password):
    # Encode the serial number and password as bytes
    serial_bytes = serial.encode()
    password_bytes = password.encode()

    # XOR the serial number and password bytes together
    encoded_bytes = bytearray(len(serial_bytes))
    for i in range(len(serial_bytes)):
        encoded_bytes[i] = serial_bytes[i] ^ password_bytes[i % len(password_bytes)]

    # Encode the resulting bytes as a base64 string
    encoded_str = base64.b64encode(encoded_bytes).decode()

    return encoded_str

def decode(encoded, password):
    # Decode the base64-encoded string as bytes
    encoded_bytes = base64.b64decode(encoded)

    # Decode the password as bytes
    password_bytes = password.encode()

    # XOR the encoded bytes and password bytes together
    serial_bytes = bytearray(len(encoded_bytes))
    for i in range(len(encoded_bytes)):
        serial_bytes[i] = encoded_bytes[i] ^ password_bytes[i % len(password_bytes)]

    # Decode the resulting bytes as a string
    serial = serial_bytes.decode()

    return serial



def check_key(key):
    # Get the serial number of the Raspberry Pi
    serial = subprocess.run(["cat", "/sys/firmware/devicetree/base/serial-number"], stdout=subprocess.PIPE, universal_newlines=True).stdout.strip().split("\n")[-1].split(":")[-1].strip()
    #print(f"Serial number: {serial}")
    # Decode the key and compare it to the serial number
    decoded = decode(key, "Q1VTQlVEQ1UGRwBCEQQAEGU=")
    if decoded == serial:
        return True
        #print("This code is running on the correct Raspberry Pi.")
    else:
        return False
        #print("This code is not running on the correct Raspberry Pi.")
        # Kill all processes or reboot the Raspberry Pi
        #os.system("sudo reboot") # reboot the system
        # or
        #os.system("killall -9 python") # kill all python process


'''serial = "00000000e5e6bacb"
password = "IgMxIyEjMyQhNCMi"
encoded = encode(serial, password)
print(f"Encoded serial number: {encoded}")

serial = subprocess.run(["cat", "/sys/firmware/devicetree/base/serial-number"], stdout=subprocess.PIPE, universal_newlines=True).stdout.strip().split("\n")[-1].split(":")[-1].strip()
#print(f"Serial number: {serial}")
password = "secret"
encoded = encode(serial, password)
#print(f"Encoded serial number: {encoded}")'''

#check_key("Q1VTQlVEQ1UGRwBCEQQAEUU=", "secret")'''

