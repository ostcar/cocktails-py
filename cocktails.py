import sys
from collections import defaultdict
from typing import Dict, Generator, Iterable, List, Optional, Set, Tuple

Ingredients = Set[str]


class Cocktail:
    name: str
    page: int
    ingredients: Ingredients

    def __init__(self, name: str, page: int, ingredients: Iterable[str]) -> None:
        self.name = name
        self.page = page
        self.ingredients = set(i for i in ingredients)

    def __repr__(self) -> str:
        return "Cocktail({}, {}, {})".format(self.name, self.page, ", ".join(self.ingredients))

    def to_json(self) -> str:
        ingredients = ",".join('"{}"'.format(i) for i in self.ingredients)
        return '{{"name":"{}","page":{},"ingredients":[{}]}}'.format(self.name, self.page, ingredients)


Cocktails = List[Cocktail]


def load_cocktails(path) -> Cocktails:
    out: Cocktails = []
    with open(path) as f:
        for line in f.readlines():
            name, page, *ingredients = line.split(',')
            out.append(Cocktail(name.strip(), int(page.strip()), [i.strip() for i in ingredients]))
    return out


def get_my_ingredients(path: Optional[str] = None) -> Ingredients:
    out: Ingredients = set()
    if path is not None:
        with open(path) as f:
            for line in f.readlines():
                if line.strip():
                    out.add(line.strip())
    else:
        while True:
            i = input()
            if i:
                out.add(i)
            else:
                break
    return out


def print_index(cocktails: Cocktails) -> None:
    for c in sorted(cocktails, key=lambda c: c.name):
        print("{}\t\t{}".format(c.name, c.page))


def print_cocktails(cocktails: Iterable[Cocktail]) -> None:
    for c in cocktails:
        print("{:<20} {}".format(c.name, c.page))


def get_ingredients(cocktails: Cocktails) -> Ingredients:
    ingredients: Ingredients = set()
    for cocktail in cocktails:
        for ingredient in cocktail.ingredients:
            ingredients.add(ingredient)
    return ingredients


def find_cocktails(cocktails: Cocktails, ingredients: Ingredients) -> Generator[Cocktail, None, None]:
    """
    List all cocktails, that can be made with the ingredients.
    """
    for cocktail in cocktails:
        if cocktail.ingredients.issubset(ingredients):
            yield cocktail


def shopping(cocktails: Cocktails, ingredients: Ingredients) -> List[Tuple[str, Cocktails]]:
    needed: Dict[str, Cocktails] = defaultdict(list)
    for cocktail in cocktails:
        diff = cocktail.ingredients.difference(ingredients)
        if len(diff) == 1:
            needed[diff.pop()].append(cocktail)
    return sorted(needed.items(), key=lambda need: len(need[1]), reverse=True)


def to_json(cocktails: Cocktails) -> str:
    """
    Returns all cocktails as json.
    """
    return "[{}]".format(",".join(cocktail.to_json() for cocktail in cocktails))


def main(argv: List[str]) -> None:
    try:
        command = argv[1]
    except IndexError:
        command = ""

    if command == "ingredients":
        cocktails = load_cocktails('cocktails.txt')
        for i in sorted(get_ingredients(cocktails)):
            print(i)

    elif command == "cocktails":
        cocktails = load_cocktails('cocktails.txt')
        my_ingredients = get_my_ingredients('vorhanden.txt')
        all_ingredients = get_ingredients(cocktails)
        if not my_ingredients.issubset(all_ingredients):
            print("Liste enthält ungültige Zutaten: {}".format(my_ingredients.difference(all_ingredients)))
            exit(1)

        print_cocktails(find_cocktails(cocktails, my_ingredients))

    elif command == "shopping":
        cocktails = load_cocktails('cocktails.txt')
        my_ingredients = get_my_ingredients('vorhanden.txt')
        all_ingredients = get_ingredients(cocktails)
        if not my_ingredients.issubset(all_ingredients):
            print("Liste enthält ungültige Zutaten: {}".format(my_ingredients.difference(all_ingredients)))
            exit(1)
        for ingredient, cocktails in shopping(cocktails, my_ingredients):
            c_list = ", ".join("{} ({})".format(cocktail.name, cocktail.page) for cocktail in cocktails)
            print("{:<20} {}".format(ingredient, c_list))

    elif command == "ingredient":
        cocktails = load_cocktails('cocktails.txt')
        if len(argv) < 3:
            print('Mindestens eine Zutat angeben')
            exit(1)
        ingredients = set(argv[2:])
        all_ingredients = get_ingredients(cocktails)
        if not ingredients.issubset(all_ingredients):
            print('Ungültige Zutat')
            exit(1)
        my_cocktails = [cocktail for cocktail in cocktails if ingredients.issubset(cocktail.ingredients)]
        print_cocktails(my_cocktails)
        print()
        print("\n".join(get_ingredients(my_cocktails)))

    elif command == "myingredient":
        cocktails = load_cocktails('cocktails.txt')
        if len(argv) < 3:
            print('Mindestens eine Zutat angeben')
            exit(1)
        ingredients = set(argv[2:])
        all_ingredients = get_ingredients(cocktails)
        if not ingredients.issubset(all_ingredients):
            print('Ungültige Zutat')
            exit(1)
        my_ingredients = get_my_ingredients('vorhanden.txt')
        cocktails = list(find_cocktails(cocktails, my_ingredients))
        my_cocktails = [cocktail for cocktail in cocktails if ingredients.issubset(cocktail.ingredients)]
        print_cocktails(my_cocktails)
        print()
        print("\n".join(get_ingredients(my_cocktails)))

    elif command == "json":
        cocktails = load_cocktails('cocktails.txt')
        print(to_json(cocktails))
    else:
        print("Usage: python cocktails.py COMMAND\nCOMMAND is one of ingredients, cocktails, shopping or ingredient")


if __name__ == '__main__':
    main(sys.argv)
