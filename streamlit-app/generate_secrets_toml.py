import json

# Read the Firebase credentials JSON file
with open('streamlit-app/config/firebase-credentials.json', 'r') as f:
    creds = json.load(f)

# Convert to TOML format for Streamlit secrets
toml_output = "[firebase]\n"
for key, value in creds.items():
    if key == 'private_key':
        # Use triple quotes for multi-line private key
        toml_output += f'{key} = """{value}"""\n'
    elif isinstance(value, str):
        # Regular string
        toml_output += f'{key} = "{value}"\n'
    else:
        toml_output += f'{key} = "{value}"\n'

print("=" * 60)
print("COPY THE TEXT BELOW INTO STREAMLIT CLOUD SECRETS:")
print("=" * 60)
print()
print(toml_output)
print()
print("=" * 60)
print("Instructions:")
print("1. Copy everything between the === lines above")
print("2. Go to Streamlit Cloud → Your App → Settings → Secrets")
print("3. Paste it into the secrets box")
print("4. Click Save")
print("=" * 60)
