import re


def split_recipes(recipes_text):
    splitters = ["\n", ",", ";"]
    splitters_cnt = [(splitter, recipes_text.count(splitter)) for splitter in splitters]
    max_splitter = max(splitters_cnt, key=lambda x: x[1])[0]
    return recipes_text.split(max_splitter)


def remove_leading_numbers(text):
    """Replace all occurences of numbers followed by a dot with an empty string"""
    return re.sub(r"\d+\.", ",", text)


def process_recipes_response(text):
    result = remove_leading_numbers(text)
    result = split_recipes(result)
    result = [item.strip().capitalize() for item in result if len(item.strip()) > 0]
    return result


print("Done")
