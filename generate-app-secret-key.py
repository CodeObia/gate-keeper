import secrets

secret_key = secrets.token_hex(32)
print(secret_key)

env_file = "./.env"
with open(env_file, 'w') as my_file:
    my_file.write(f"FLASK_SECRET_KEY={secret_key}")

print("Secret key generated and stored...")
