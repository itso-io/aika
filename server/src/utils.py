import os


def get_file_full_path(relative_to_root):
  return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_to_root)
