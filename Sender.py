import socket
import time 
import struct

receiverIP = '192.168.1.111'
receiverPort = 12600
MSS = 8192
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
timeout = 3

file = open('large_file.jpeg', 'rb')
image_data = file.read(MSS)

window_size = 20
packet_screen = [] 

start_time = time.time()
last_ack_received = -1 
packet_id = 0
file_id = 0

while True:
    while len(packet_screen) < window_size and image_data:
        if not image_data:
            trailer = 0xFFFF
        else:
            trailer = 0x0000
        
        packet = struct.pack('!HH8192sI', packet_id, file_id, image_data, trailer)
        client.sendto(packet, (receiverIP, receiverPort))
        print(f"Sent packet with sequence number: {packet_id}")
        packet_id += 1
        packet_screen.append(packet)
        image_data = file.read(MSS)
        
    if time.time() - start_time >= timeout:
        print("Timeout: No ACK")
        start_time = time.time()
        continue

    ack, _ = client.recvfrom(1024)

    if ack != b'ACK':
        print("Error in ACK")

    last_ack_received = struct.unpack('!H', ack)[0]

    while packet_screen and struct.unpack('!H', packet_screen[0][2:4])[0] <= last_ack_received:
        packet_screen.pop(0)


    if not packet_screen and not image_data:
        break

file.close()
