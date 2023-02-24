import logging
import random
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List

import numpy as np
import pandas as pd

from exceptions import NotEnoughItemsException

logger = logging.getLogger("generator")


@dataclass
class Generator:
    path_to_item_file: str

    @cached_property
    def items(self) -> Dict[str, List[str]]:
        items = {}
        items_df = pd.read_excel(self.path_to_item_file)
        items_df.replace({np.nan: ""})
        for items_column in items_df.columns:
            items[items_column] = list(set([item for item in items_df[items_column].to_list() if item]))

        return items

    @cached_property
    def number_of_items_per_category(self) -> List[int]:
        n_categories = len(self.items.keys())
        rest_items = 25 % n_categories
        number_of_items_per_category = [25 // n_categories for _ in range(n_categories)]
        number_of_items_per_category[random.randint(0, n_categories - 1)] += rest_items
        return number_of_items_per_category

    def generate_samples(self, number_of_samples: int = 100):
        samples = [self.generate_one_sample() for _ in range(number_of_samples)]

    def generate_one_sample(self):
        items_sample = self.get_items_for_one_sample()
        random.shuffle(items_sample)
        items_df = self.create_df_from_items(items_sample)
        items_html = items_df.to_html()
        return items_html


    def get_items_for_one_sample(self) -> List[str]:
        items_sample = []
        for number_of_items, items in zip(self.number_of_items_per_category, self.items.values()):
            if number_of_items > (length := len(items)):
                logger.error(f"Requested to sample {number_of_items} from item category with {length} items.")
                raise NotEnoughItemsException
            items_sample.extend(random.sample(items, number_of_items))
        return items_sample

    @staticmethod
    def create_df_from_items(items: List[str]) -> pd.DataFrame:
        dimension = int(np.sqrt(len(items)))
        items_array = np.array(items).reshape(dimension, dimension)
        return pd.DataFrame(items_array)