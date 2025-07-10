from enum import StrEnum, Enum
from rich import print as rprint
from typing import TypeVar




class NewCategories(StrEnum):
    STONE = "Stone or Gravel"
    WOOD = "Wood"
    STEEL = "Steel"

# TODO move to json file? -> element -> category mapping 
revised_categories = {
    NewCategories.STONE: [
        "Rip-rap (Armor Rock)",
        'Stabilized Crushed Stone Paving - 4" (100mm) Depth',
        "Compacted Aggregate Base",
        "Asphalt Paving",
        "Stone Boulders",
    ],
    NewCategories.WOOD: ["Decking", "Wood Post", "Salvaged Wood", "Wood Post"],
    NewCategories.STEEL: ["Steel Guardrail", "Steel Guardrail"],
}

# TODO map to pairs.. # TODO what if cant find?
TEnum = TypeVar('TEnum', bound=Enum)
Tstr = TypeVar('Tstr', bound=str)

def create_pairs(mapping:dict[TEnum, list[Tstr]]):
    lst = []
    for key, value in mapping.items():
        for element in value:
            lst.append((element, key))
    return lst

if __name__ == "__main__":
    r = create_pairs(revised_categories)
    rprint(r)