import socket
import struct

serverPort = 12600
packet_count = 0

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', serverPort))

file = open('server_image_Large2.jpeg', "wb")

while True:
    image_chunk, client_address = server.recvfrom(8250)
    packet_id, file_id, data, trailer = struct.unpack('!HH8192sI', image_chunk)

    if trailer == 0xFFFF:
        file.write(data)
        print("File received.")
        break

    packet_count += 1
    if packet_count % 38 == 0:
        print("Simulated packet loss")
        continue

    print("Received packet from:", client_address)
    print("Packet size:", len(data))
    print("packet_count:", packet_count)
    
    file.write(data)
    server.sendto(struct.pack('!H', packet_id), client_address)

file.close()

input_file = 'server_image_Large2.jpeg'
output_file = 'restored_image.jpeg'

with open(input_file, 'rb') as binary_file:
    binary_data = binary_file.read()

with open(output_file, 'wb') as image_file:
    image_file.write(binary_data)

print("Image restored", output_file)
