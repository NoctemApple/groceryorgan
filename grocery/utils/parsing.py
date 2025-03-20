def parse_grocery_text(text):
    """
    Parses the raw text input into a list of items.
    Each non-blank line becomes an item with a 'category' index.
    The category increments each time a blank line is encountered.
    """
    items = []
    group = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            items.append({
                'name': stripped,
                'category': group,
                'done': False,
                'order': None,
                'last_done_date': None
            })
        else:
            group += 1
    return items
