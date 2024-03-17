
import random
import string

def test_response(user_input):
  length = len(user_input)
  letters = string.ascii_letters + string.digits
  return ''.join(random.choice(letters) for _ in range(length))
