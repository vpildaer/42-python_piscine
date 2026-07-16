from .light_spellbook import light_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    valid: list[str] = light_spell_allowed_ingredients()
    ing_list: list[str] = ingredients.split(', ')
    for elem in ing_list:
        if any(elem.capitalize() == i.capitalize() for i in valid):
            return "VALID"
        else:
            continue
    return "INVALID"
