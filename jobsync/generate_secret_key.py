
import secrets

def generate_secret_key():
    return ''.join(secrets.choice(
        'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50))

print(generate_secret_key())