from config.database import add_admin

# Create first admin account
admin_email = "hunterdii9879@gmail.com"
admin_password = "codesownway0707"  # Change this to a secure password

if add_admin(admin_email, admin_password):
    print(f"Admin account created successfully: {admin_email}")
else:
    print("Failed to create admin account")
