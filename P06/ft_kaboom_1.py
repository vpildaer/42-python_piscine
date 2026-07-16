if __name__ == "__main__":
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    import alchemy.grimoire.dark_spellbook as dark
    print("Testing record dark spell: ", end="")
    res: str = dark.dark_spell_record('Fantasy', 'Earth, wind and fire')
    print(res)
