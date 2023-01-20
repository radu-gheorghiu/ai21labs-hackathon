import streamlit as st
from utils.utilities import process_recipes_response
from apis.stablediffusion.stable_diffusion import StableDiffussion
from apis.ai21labs.ai21_labs import AI21Labs
from apis.clarifai.clarifai import Clarifai

if "started" not in st.session_state:
    st.session_state["started"] = True
    story_text = []

    sd = StableDiffussion()
    clarifai = Clarifai()
    ai21_labs = AI21Labs()

    st.session_state["img_path"] = sd(
        "A very realistic image of the inside a fridge, with different food items, vegetables, dairy and meats, a large variety"
    )
    st.session_state["ingredients"] = clarifai(st.session_state["img_path"])
    st.session_state["recipe_ingredients"] = None
    st.session_state["ai21labs"] = ai21_labs
    st.session_state["clarifai"] = clarifai
    st.session_state["sd"] = sd


def display_image():
    st.image(st.session_state["img_path"], use_column_width=True)
    if "clicked_fridge" not in st.session_state:
        st.session_state["clicked_fridge"] = True


def add_ingredient_to_list(ingredient):
    if ingredient in st.session_state["recipe_ingredients"]:
        st.session_state["recipe_ingredients"].remove(ingredient)
    else:
        st.session_state["recipe_ingredients"].add(ingredient)


def main():
    st.session_state["started"] = True
    ai21_labs = st.session_state["ai21labs"]
    clarifai = st.session_state["clarifai"]
    sd = st.session_state["sd"]

    no_recipes_found = 0

    story_text = []
    text_1 = "It's been a long day and you come home to prepare dinner..."
    if "text_1" in st.session_state:
        st.write(text_1)
    else:
        st.session_state["text_1"] = True
        story_text.append(text_1)
        st.write(text_1)

    text_2 = "You go into the kitchen and head towards the fridge..."
    story_text.append(text_2)
    if "text_2" in st.session_state:
        st.write(text_2)
    else:
        st.session_state["text_2"] = True
        story_text.append(text_2)
        st.write(text_2)

    clicked_fridge = st.button(
        label="Look into the fridge", disabled="clicked_fridge" in st.session_state
    )
    if clicked_fridge or "clicked_fridge" in st.session_state:
        display_image()

    if (
        clicked_fridge
        or "clicked_fridge" in st.session_state
        or "selected_recipe" in st.session_state
    ):
        options = st.multiselect(
            "Please select some ingredients", st.session_state["ingredients"]
        )

        clicked_suggest_recipe = st.button(
            label="Suggest recipes with selected ingredients",
            disabled="selected_recipe_ingredients" in st.session_state.keys(),
        )
        if clicked_suggest_recipe:
            st.session_state["recipes"] = None
            st.session_state["clicked_prepare_recipe"] = True
            st.session_state["recipe_ingredients"] = list(set(options))
            all_ingredients = ", ".join(options)
            recipes = ai21_labs(
                endpoint="completion",
                prompt_type="suggest_recipes",
                input=[all_ingredients],
            )
            clean_recipes = process_recipes_response(recipes)

            while len(clean_recipes) < 3:
                recipes2 = ai21_labs(
                    endpoint="completion",
                    prompt_type="suggest_recipes",
                    input=[all_ingredients],
                )
                inner_clean_recipes = process_recipes_response(recipes2)

                for item in inner_clean_recipes:
                    clean_recipes.append(item)
                clean_recipes = list(set(clean_recipes))
                clean_recipes = [recipe.replace("\n", " ") for recipe in clean_recipes]
                no_recipes_found += 1
                if no_recipes_found > 5:
                    st.write(
                        "No recipes found for these ingredients, please select a different ingredients"
                    )
                    clean_recipes = []
                    break
            st.session_state["recipes"] = clean_recipes

        selected_recipe = None
        if "clicked_prepare_recipe" in st.session_state:
            selected_recipe = st.radio(
                "Please select a recipe", st.session_state["recipes"]
            )
            st.session_state["selected_recipe"] = selected_recipe
            st.session_state["clicked_prepare_recipe"] = False

        if selected_recipe is not None:
            st.write(f"What ingredients do I need for {selected_recipe}?")
            click_find_out = st.button(
                "Find out", disabled="found_missing_ingredients" in st.session_state
            )
            if click_find_out:
                ingredients_selected_recipe = ai21_labs(
                    endpoint="completion",
                    prompt_type="generate_ingredients",
                    input=[selected_recipe],
                )
                selected_recipe_ingredients = ingredients_selected_recipe.split("||")
                selected_recipe_ingredients = [
                    ing.replace(",", "").strip() for ing in selected_recipe_ingredients
                ]
                for ingredient in selected_recipe_ingredients:
                    st.write("- ", ingredient)
                    st.session_state[
                        "selected_recipe_ingredients"
                    ] = selected_recipe_ingredients
            elif "selected_recipe_ingredients" in st.session_state:
                for ingredient in st.session_state["selected_recipe_ingredients"]:
                    st.write("- ", ingredient)

            if click_find_out or "selected_recipe_ingredients" in st.session_state:
                clicked_find_missing_ingredients = st.button(
                    "Find out what ingredients I'm missing",
                    disabled="go_to_grocery_img" in st.session_state,
                )
                if (
                    "found_missing_ingredients" in st.session_state
                    or clicked_find_missing_ingredients
                ):
                    ingredients_i_have = "\n".join(
                        st.session_state["recipe_ingredients"]
                    ).lower()
                    ingredients_recipe = "\n".join(
                        st.session_state["selected_recipe_ingredients"]
                    ).lower()
                    missing_ingredients = ai21_labs(
                        endpoint="completion",
                        prompt_type="list2_vs_list1",
                        input=[ingredients_i_have, ingredients_recipe],
                    )
                    print("You are missing", missing_ingredients)
                    st.write("You are missing the following ingredients:")
                    st.write(missing_ingredients)
                    st.session_state["found_missing_ingredients"] = missing_ingredients

                    if st.session_state["found_missing_ingredients"]:
                        clicked_go_to_grocery = st.button(
                            "Go to the grocery",
                            disabled="go_to_grocery_img" in st.session_state,
                        )
                        if (
                            clicked_go_to_grocery
                            and "go_to_grocery_img" not in st.session_state
                        ):
                            st.session_state["go_to_grocery_img"] = sd(
                                f"A very realistic image of a man in a grocery with {st.session_state['found_missing_ingredients']}"
                            )
                        if "go_to_grocery_img" in st.session_state:
                            st.image(st.session_state["go_to_grocery_img"])
                            text_4 = "Now we have all the ingredients, it's time to start cooking."
                            st.write(text_4)
                            clicked_start_cooking = st.button(
                                "Start cooking",
                                disabled="start_cooking_img" in st.session_state,
                            )
                            if (
                                clicked_start_cooking
                                and "start_cooking_img" not in st.session_state
                            ):
                                st.session_state["start_cooking_img"] = sd(
                                    f"{st.session_state['selected_recipe']}"
                                )
                            if "start_cooking_img" in st.session_state:
                                st.image(st.session_state["start_cooking_img"])
                                text_5 = "This food looks great, thank you for recommending it!"

                                story_text.append(
                                    f"and found {', '.join(st.session_state['recipe_ingredients'])}. Probably I could make {st.session_state['selected_recipe']}, but still need {st.session_state['found_missing_ingredients']}. I'll go to the store. Got back, {text_4}. {text_5}"
                                )
                                text_6 = "If you enjoyed the meal, share your excitement with a short story about your day"
                                st.write(text_6)
                                clicked_summarize = st.button(
                                    "Today in a nutshell",
                                    disabled="clicked_summarize" in st.session_state,
                                )
                                if (
                                    clicked_summarize
                                    and "summary" not in st.session_state
                                ):
                                    story = " ".join(story_text)
                                    st.session_state["summary"] = ai21_labs(
                                        "summarize", story
                                    )
                                if "summary" in st.session_state:
                                    st.write(st.session_state["summary"])
                                    text_7 = "Share this story in a tweet"
                                    st.write(text_7)
                                    hashtags = ai21_labs(
                                        endpoint="completion",
                                        prompt_type="suggest_hashtags",
                                        input=[st.session_state["summary"]],
                                    )
                                    st.write(hashtags)
                                    clicked_tweet_post = st.button(
                                        "Post to tweet",
                                        disabled="posted_to_tweet" in st.session_state,
                                    )
                                    if (
                                        clicked_tweet_post
                                        and "posted_to_tweet" not in st.session_state
                                    ):
                                        st.session_state["posted_to_tweet"] = True
                                        # auth = tweepy.OAuthHandler(api_key,api_secrets)
                                        # auth.set_access_token(access_token,access_secret)
                                        # api = tweepy.API(auth, wait_on_rate_limit=True)
                                        # mention = '@AI21Labs'
                                        # status = mention + st.session_state["summary"] + hashtags
                                        # api.update_status(status=status)


if __name__ == "__main__":
    main()
