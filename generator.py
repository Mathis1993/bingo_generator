import logging
import random
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List

import numpy as np
import pandas as pd
from exceptions import NotEnoughItemsException
from weasyprint import CSS, HTML

logger = logging.getLogger("generator")


@dataclass
class Generator:
    path_to_item_file: str = "./items.xlsx"
    path_to_html_file: str = "./bingo.html"
    path_to_css_file: str = "./bingo.css"
    creation_counter: int = 0

    @cached_property
    def items(self) -> Dict[str, List[str]]:
        items = {}
        items_df = pd.read_excel(self.path_to_item_file)
        items_df = items_df.replace({np.nan: None})
        for items_column in items_df.columns:
            items[items_column] = list(
                set([item for item in items_df[items_column].to_list() if item])
            )

        return items

    @cached_property
    def number_of_items_per_category(self) -> List[int]:
        n_categories = len(self.items.keys())
        rest_items = 25 % n_categories
        number_of_items_per_category = [25 // n_categories for _ in range(n_categories)]
        number_of_items_per_category[random.randint(0, n_categories - 1)] += rest_items
        return number_of_items_per_category

    @cached_property
    def html(self) -> str:
        with open(self.path_to_html_file, "r") as f:
            return f.read()

    def generate_samples(self, number_of_samples: int = 100):
        self.creation_counter = 0
        [self.generate_one_sample() for _ in range(number_of_samples)]

    def generate_one_sample(self):
        items_sample = self.get_items_for_one_sample()
        random.shuffle(items_sample)

        cells = [
            f"""
            <label>
              <input type="checkbox">
              <div class="mark"><span>{item}</span></div>
            </label>"""
            for item in items_sample
        ]
        cells = "".join(cell for cell in cells)

        html_string = self.insert_items_into_html(cells)
        self.create_pdf_file(html_string)

    def get_items_for_one_sample(self) -> List[str]:
        items_sample = []
        for number_of_items, items in zip(
            self.number_of_items_per_category, self.items.values()
        ):
            if number_of_items > (length := len(items)):
                logger.error(
                    f"Requested to sample {number_of_items} from item category with {length} items."
                )
                raise NotEnoughItemsException
            items_sample.extend(random.sample(items, number_of_items))
        return items_sample

    def insert_items_into_html(self, items_html: str) -> str:
        first_part, second_part = self.html.split("<small>")
        return first_part + items_html + "<small>" + second_part

    def create_pdf_file(self, html_string: str):
        self.creation_counter += 1
        with open(f"bingo_{self.creation_counter}.html", 'w') as f:
            f.write(html_string)
        # weasyprint does somehow not respect the alignment of the cells
        # html = HTML(string=html_string, base_url="./")
        # css = CSS(filename=self.path_to_css_file)
        # html.write_pdf(
        #     target=f"bingo_{self.creation_counter}.pdf", stylesheets=[css]
        # )
