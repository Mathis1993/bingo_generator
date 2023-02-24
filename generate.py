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
    args = parser.parse_args()
    number = 10
    if args.number:
        number = int(args.number)

    g = Generator()
    g.generate_samples(number)


if __name__ == '__main__':
    generate_bingo_pdf_files()

