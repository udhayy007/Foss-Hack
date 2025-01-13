from config.database import add_admin
from dotenv import load_dotenv
import os

load_dotenv()

# Create first admin account
admin_email = os.getenv('ADMIN_EMAIL')
admin_password = os.getenv('ADMIN_PASSWORD')

print(admin_email)
print(admin_password)

# if add_admin(admin_email, admin_password):
#     print(f"Admin account created successfully: {admin_email}")
# else:
#     print("Failed to create admin account")
