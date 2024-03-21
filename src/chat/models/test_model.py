
import random
import string

def test_response():
  length = 10
  letters = string.ascii_letters + string.digits
  return ''.join(random.choice(letters) for _ in range(length))
