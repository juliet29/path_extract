from enum import StrEnum
from rich import print as rprint


class NewCategories(StrEnum):
    STONE = "Stone or Gravel"
    WOOD = "Wood"
    STEEL = "Steel"

# TODO move to json file? 
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

def create_pairs(mapping:dict):
    lst = []
    for key, value in revised_categories.items():
        for element in value:
            lst.append((element, key.value))
    return lst

if __name__ == "__main__":
    r = create_pairs(revised_categories)
    rprint(r)