import os
import sys

def prepare_data_dir(subdir):
    data_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "./../data/"+subdir))

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return data_dir
