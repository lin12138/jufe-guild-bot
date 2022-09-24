filename = "./data/msg_id.txt"
def set_msg_id(msg_id: str):
    with open(filename, 'w') as f:
        f.write(msg_id)

def get_msg_id():
    with open(filename, 'r') as f:
        return f.read()
