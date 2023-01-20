import requests
import json

API_KEY = "<ADD YOUR KEY HERE>"


class AI21Labs:
    def __init__(self):
        with open("apis/ai21labs/completion_params.json", "r") as json_file:
            self._params = json.load(json_file)

    def __call__(self, endpoint, input, prompt_type=None):
        if endpoint == "completion":
            return self._call_completion_api(prompt_type, input)
        elif endpoint == "summarize":
            return self._call_summarize_api(input)
        else:
            raise Exception("Invalid request")

    def _call_completion_api(self, prompt_type, input):
        params = self._params[prompt_type]
        print(params["prompt"].format(*input))
        response = requests.post(
            url=f"https://api.ai21.com/studio/v1/experimental/{params['model']}/complete",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "prompt": params["prompt"].format(*input),
                "numResults": params["numResults"],
                "maxTokens": params["maxTokens"],
                "temperature": params["temperature"],
                "topKReturn": params["topKReturn"],
                "topP": params["topP"],
                "countPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False,
                },
                "frequencyPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False,
                },
                "presencePenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False,
                },
                "stopSequences": params["stopSequences"],
            },
        )
        recipes = json.loads(response.text)["completions"][0]["data"]["text"]
        return recipes

    def _call_summarize_api(self, prompt):
        response = requests.post(
            url="https://api.ai21.com/studio/v1/experimental/summarize",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "text": prompt,
            },
        )
        return json.loads(response.text)["summaries"][0]["text"]


def load_params():
    with open("completion_params.json", "r") as json_file:
        params = json.load(json_file)
    return params


def main():
    ai21_api_call = AI21Labs()
    params = load_params()
    # 1. Suggest recipe
    # input = [", ".join(ingredients)]
    ingredients = "ham, parsley, milk, smoked salmon, cheese, tomatoes, cucumber, steak, pasta, flour"
    input = [ingredients]
    print(params["suggest_recipes"]["prompt"].format(*input))
    suggest_recipe_result = ai21_api_call("completion", input, "suggest_recipes")
    print(suggest_recipe_result)
    print("==========================================")
    # 2. Generate ingredients for recipe
    recipe = "Smoked Salmon and Cheese"
    input = [recipe]
    print(params["generate_ingredients"]["prompt"].format(*input))
    generate_ingredients_result = ai21_api_call(
        "completion", input, "generate_ingredients"
    )
    print(generate_ingredients_result)
    print("==========================================")
    # 3. List 2 vs list 1
    lists = "List 1:\n1/2 cup flour\n1/2 cup yeast\n1/2 cup shredded cheddar cheese\n\nList 2:\n1/2 cup of grilled chicken\n1/2 cup of pasta\n1/2 cup shredded cheddar cheese\n1/2 cup water\n\n"
    input = [lists]
    print(params["list2_vs_list1"]["prompt"].format(*input))
    list2_vs_list1_result = ai21_api_call("completion", input, "list2_vs_list1")
    print(list2_vs_list1_result)
    print("==========================================")
    # 4. Remove allergens
    remove_list = '"milk" and "eggs" and "flour"'
    from_list = "ham, parsley, milk, smoked salmon, cheese, tomatoes, cucumber, steak, pasta, flour, eggs"
    input = [remove_list, from_list]
    print(params["remove_allergens"]["prompt"].format(*input))
    remove_allergens_result = ai21_api_call("completion", input, "remove_allergens")
    print(remove_allergens_result)
    print("==========================================")
    # 5. Summarize
    prompt = "Peloneustes is a genus of pliosaurid plesiosaur from the Middle Jurassic of England, known from the Oxford Clay Formation. Its sole species was originally named Plesiosaurus philarchus by Harry Govier Seeley in 1869 before Richard Lydekker gave it its own genus in 1889. It is known from many specimens, some very complete. It had a total length of 3.5 to 4 metres (11 to 13 ft), and a large, triangular skull elongated into a narrow snout with conical teeth. The two sides of its mandible (lower jaw) were fused into a long symphysis at the front. Its neck was short for a plesiosaur and its limbs were modified into flippers, with the back pair larger than the front. Peloneustes is classified in Thalassophonea with other short-necked pliosaurids. It was well-adapted to aquatic life, using its flippers for swimming, and its skull was reinforced against the stresses of feeding. Peloneustes's long, narrow snout could have been swung through the water to catch fish with its sharp teeth."
    print(prompt)
    summary = ai21_api_call("summarize", prompt)
    print(summary)
    print("==========================================")
    # 6. Suggest hashtags
    input = [summary]
    print(params["suggest_hashtags"]["prompt"].format(*input))
    suggest_hashtags_result = ai21_api_call("completion", input, "suggest_hashtags")
    print(suggest_hashtags_result)
