import argparse
import logging
from pathlib import Path
from shutil import move
from threading import Thread
from queue import Queue


def del_empty_folders(folder: Path) -> bool:
    for el in folder.iterdir():
        if el.is_dir():
            if del_empty_folders(el):
                el.rmdir()
        else:
            return False
    return True


def get_arguments() -> tuple[Path, Path]:
    """
    --source [-s] folder
    --output [-o]
    """
    parser = argparse.ArgumentParser(description='Sorting folder')
    parser.add_argument('--source', '-s', help='Source folder', required=True)
    parser.add_argument('--output', '-o', help='Output folder', default='sorted_trash')
    args = vars(parser.parse_args())

    base_folder = Path(args.get('source'))
    if not base_folder.exists():
        logging.error(f"Don't exist folder {base_folder}")
        quit()

    output_folder = Path(args.get('output'))
    if not make_folder(output_folder):
        quit()

    return base_folder, output_folder


def grabs_files(path: Path, files_queue: Queue) -> None:
    # logging.info(f'grabs_files: {path}')
    for file in path.iterdir():
        if file.is_file():
            files_queue.put(file)


def grabs_folder(path: Path, folders_queue: Queue) -> None:
    # logging.info(f'grabs_folder: {path}')
    folders_queue.put(path)
    for folder in path.iterdir():
        if folder.is_dir():
            grabs_folder(folder, folders_queue)


def make_folder(folder: Path) -> bool:
    try:
        folder.mkdir(exist_ok=True, parents=True)
    except OSError as err:
        logging.error(err)
        return False
    return True


def move_file(file: Path, output_folder: Path) -> None:
    # logging.info(f'moving_files: {file}')
    ext = file.suffix
    new_path = output_folder / ext
    if make_folder(new_path):
        move(file, new_path / file.name)


def main():

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    folders_queue = Queue()
    files_queue = Queue()
    base_folder, output_folder = get_arguments()

    grabs_folder(base_folder, folders_queue)
    # --------------------------------------------
    th_folder_list = []
    while not folders_queue.empty():
        th_folder = Thread(target=grabs_files, args=(folders_queue.get(), files_queue))
        th_folder.start()
        th_folder_list.append(th_folder)
    [th.join() for th in th_folder_list]

    th_move_file_list = []
    while not files_queue.empty():
        th_move_file = Thread(target=move_file, args=(files_queue.get(), output_folder))
        th_move_file.start()
        th_move_file_list.append(th_move_file)
    [th.join() for th in th_move_file_list]

    del_empty_folders(base_folder)


if __name__ == '__main__':
    main()
