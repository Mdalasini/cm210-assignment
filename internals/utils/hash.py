import hashlib

def hash(password: str) -> str:
  base = hashlib.md5(password.encode()).hexdigest()
  rotated = ''.join(
    format((int(c, 16) + i) % 16, 'x')
    for i, c in enumerate(base)
  )
  reversed_hash = rotated[::-1]
  return reversed_hash