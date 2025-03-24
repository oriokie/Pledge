from app.core.security import get_password_hash, verify_password

# Test password hashing
password = "admin123"
hashed = get_password_hash(password)
print(f"Original password: {password}")
print(f"Hashed password: {hashed}")
print(f"Verification result: {verify_password(password, hashed)}")

# Test with known hash from database
known_hash = "$2b$12$3F/r1xwb6doKVy8EA5anIuqwObX.dhkyJVIxC.cJ675LAJAkMt0Na"
print(f"\nVerification with known hash: {verify_password(password, known_hash)}") 