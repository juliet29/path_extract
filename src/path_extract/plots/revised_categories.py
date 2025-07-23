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
# TODO now this is overly general..
TEnum = TypeVar("TEnum", bound=Enum)
Tstr = TypeVar("Tstr", bound=str)

if __name__ == "__main__":
    pass
