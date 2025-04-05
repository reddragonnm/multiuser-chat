import json

PAYLOAD_SIZE_BYTES = 2


def decode_packet(encoded_data):
    json_data = encoded_data[PAYLOAD_SIZE_BYTES:].decode()
    return json.loads(json_data)


def encode_packet(json_data):
    data_bytes = json.dumps(json_data).encode()
    payload_size = len(data_bytes).to_bytes(2)
    return payload_size + data_bytes


def get_next_packet(buffer):
    if len(buffer) >= PAYLOAD_SIZE_BYTES:
        payload_size = int.from_bytes(buffer[:PAYLOAD_SIZE_BYTES])
        if len(buffer) >= PAYLOAD_SIZE_BYTES + payload_size:
            encoded_data = buffer[: PAYLOAD_SIZE_BYTES + payload_size]
            new_buffer = buffer[PAYLOAD_SIZE_BYTES + payload_size :]
            payload = decode_packet(encoded_data)

            return payload, new_buffer
