# bingo_generator

Generate pdf bingo cards to print for your party from an item pool (`items.xlsx` per default).

![bingo card example](sample_bingo.png)

## Usage
1. Create and activate a virtual environment, e.g. by running `python -m venv venv && source venv/bin/activate` (bash).
2. Install the required packages by running `pip install -r requirements.txt`.
3. Generate bingo files by running `python generate.py`

Arguments:
- `-n`: Number of bingo versions to produce (10 by default)
- `-p`: Path to the `.xlsx` file containing the items (`./items.xlsx` by default) 
