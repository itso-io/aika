# Native
import os
import random
import string
from hashlib import md5

# Installed
## N/A

# From app
## N/A

def random_password():
    """Generate a random password """
    randomSource = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice('!#$%&\()*+,-./:;<=>?@[\\]^_{|}~')

    for i in range(6):
        password += random.choice(randomSource)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password


def get_file_full_path(relative_to_root):
  return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_to_root)


def md5_hash(s):
  return md5(s.encode()).hexdigest()
