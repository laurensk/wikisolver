import requests
from tqdm import tqdm
import sys
import os
from utils import data_dir_utils

def main():
    if len(sys.argv) != 2:
            print("Usage: python download_dump.py <language_code>")
            sys.exit(1)
        
    language_code = sys.argv[1]

    dumps_dir = data_dir_utils.prepare_data_dir("dumps")

    response = requests.get("https://dumps.wikimedia.org/index.json")
    json_data = response.json()

    jobs = json_data['wikis'][language_code+"wiki"]['jobs']
    sub = jobs.get('articlesdumprecombine', jobs.get('articlesdump'))

    file_info = sub['files'][list(sub['files'].keys())[0]]
    url = file_info['url']

    full_url = "https://dumps.wikimedia.org" + url
    file_name = full_url.split("/")[-1]

    print(f"Downloading {file_name} from {full_url} - please wait...")

    with requests.get(full_url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(os.path.join(dumps_dir, file_name), 'wb') as f, tqdm(
            desc=file_name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

    print("Done!")

if __name__ == "__main__":
    main()
