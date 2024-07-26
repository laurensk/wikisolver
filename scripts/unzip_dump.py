import bz2
import shutil
import sys
from utils import data_dir_utils
import os

def main():
    if len(sys.argv) != 2:
            print("Usage: python unzip_dump.py <dump_name>")
            sys.exit(1)
        
    dump_name = sys.argv[1]
    output_name = dump_name.replace('.bz2', '')

    dumps_dir = data_dir_utils.prepare_data_dir("dumps")

    print("Decompressing, please wait...")

    with bz2.BZ2File(os.path.join(dumps_dir, dump_name), 'rb') as file, open(os.path.join(dumps_dir, output_name), 'wb') as out_file:
        shutil.copyfileobj(file, out_file)

    print("Decompression completed!")

if __name__ == "__main__":
    main()
