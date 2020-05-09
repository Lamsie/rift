#!../venv/bin/python3
import os
import shutil

import click
import requests

from pathlib import Path

from tqdm import tqdm


DS_URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'


@click.command()
@click.option('--extract-to',
              type=click.Path(exists=False, file_okay=False, dir_okay=True, writable=True, readable=True,
                              resolve_path=False, allow_dash=False, path_type=str),
              default='../datasets/',
              show_default=True,
              help='Path to the directory to unpack the archive.')
def download(extract_to):
    """Download LFW Dataset archive and unpack its content into the given folder."""
    try:
        extract_to = Path(extract_to)
        archive_path = extract_to / 'lfw.tgz'
        with open(archive_path, 'wb') as archive:
            print('Downloading Labeled Faces in the Wild...')
            response = requests.get(DS_URL, stream=True)
            total_bytes = response.headers.get('Content-Length')

            if total_bytes is None:
                archive.write(response.content)
            else:
                with tqdm(total=int(total_bytes), unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        archive.write(chunk)
                        pbar.update(len(chunk))
        
        print('Unpacking...')
        shutil.unpack_archive(archive_path, extract_to)
        print('Done')

    finally:
        os.remove(archive_path)


if __name__ == '__main__':
    download()

