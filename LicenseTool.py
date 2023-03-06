import base64
import subprocess
import os

def encode(serial, password):
    serial_bytes = serial.encode()
    password_bytes = password.encode()

    encoded_bytes = bytearray(len(serial_bytes))
    for i in range(len(serial_bytes)):
        encoded_bytes[i] = serial_bytes[i] ^ password_bytes[i % len(password_bytes)]

    encoded_str = base64.b64encode(encoded_bytes).decode()

    return encoded_str

def decode(encoded, password):
    encoded_bytes = base64.b64decode(encoded)

    password_bytes = password.encode()

    serial_bytes = bytearray(len(encoded_bytes))
    for i in range(len(encoded_bytes)):
        serial_bytes[i] = encoded_bytes[i] ^ password_bytes[i % len(password_bytes)]

    serial = serial_bytes.decode()

    return serial



def check_key(password):
    if len(password) < 16:
        return False
    serial = subprocess.run(["cat", "/sys/firmware/devicetree/base/serial-number"], stdout=subprocess.PIPE, universal_newlines=True).stdout.strip().split("\n")[-1].split(":")[-1].strip()
    # Decode the key and compare it to the serial number
    decoded = decode("eVd9SHlJdVooTDReLCIuC0k=", password)
    if decoded == serial:
        print("This code is running on the correct Raspberry Pi.")
        return True
    else:
        print("This code is not running on the correct Raspberry Pi.")
        return False
        # Kill all processes or reboot the Raspberry Pi
        #os.system("sudo reboot") # reboot the system
        # or
        #os.system("killall -9 python") # kill all python process


