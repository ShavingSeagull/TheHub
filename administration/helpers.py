# -----------------------------------------
# Helper methods for the Administration app
# -----------------------------------------

def category_name_converter(category_name: str) -> str:
    """
    Takes a human-readable category name ('friendly name')
    and converts it to a machine-friendly version. Used when
    adding new categories. Also removes punctuation.

    Eg: Learning Success! -> learning_success

    Params
    ------
    category_name: str
        The friendly name to be converted

    return_type: str
    """
    stripped_name = category_name.strip()
    formatted_name = ""

    for char in stripped_name:
        if char.isalnum():
            formatted_name += char
        if char == ' ':
            formatted_name += '_'
    
    return formatted_name.lower()
