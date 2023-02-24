import argparse

from generator import Generator


def generate_bingo_pdf_files():
    parser = argparse.ArgumentParser(
        description="Bingo Generator generating html files."
    )
    parser.add_argument(
        "-n",
        "--number",
        type=str,
        help="Number of bingo files to produce."
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path to .xlsx file containing the items."
    )
    args = parser.parse_args()
    number = 10
    path = "./items.xlsx"
    if args.number:
        number = int(args.number)
    if args.path:
        path = args.path

    g = Generator(path_to_item_file=path)
    g.generate_samples(number)


if __name__ == '__main__':
    generate_bingo_pdf_files()

