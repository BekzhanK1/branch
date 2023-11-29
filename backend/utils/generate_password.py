import uuid

def generate_password():
    return uuid.uuid4().hex[:10]