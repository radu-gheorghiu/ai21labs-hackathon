# KitchenGenie

## AI21Lab's hackathon - January 2023

### Quick Install
Installing the aplication is done by cloning this repository and then running:

`pip install -r requirements.txt`

`pip install clarifai-grpc==8.11.0`

`pip install protobuf==3.19.5`

### 🤔 What is this?

This application is built on top of AI21Lab's Large Language Models and uses them as knowledge bases to help you reduce food waste and use existing ingredients in creative ways.

### 📖 Documentation

How-to example: [A demo of how to interact with the application](https://www.youtube.com/playlist?list=PLmbqa7kiU8F9fGVrEcKu9NY_RRYbwLHWv)

#### Running the application locally

- install Python 3.9.8 or newer
- install the requirements for the environment mentioned above in the Quick Install
- create your own KEY and SECRET for the following services: Stability AI (Stable Difussion - Dreambooth), Clarifai, AI21Labs
- in each of the Python modules in the **apis** package, also mentioned above, add the KEY and SECRET values.
        
        `os.environ["STABILITY_KEY"] = "<YOUR STABILITY KEY HERE>"` - for Stability AI (stable_difussion.py)
        
        `PAT = "<ADD YOUR KEY HERE>"` - for Clarifai (clarifai.py)
        
        `API_KEY = "<ADD YOUR KEY HERE>"` - for AI21Labs (ai21_labs.py)
        
- open a command terminal and run `streamlit run app.py`
- a web browser and tab should open with the application already running (please wait a few seconds at the beginning while our first API calls and processing is done)

#### Structure of the application

- app.py - is the main Python module and the entry point in the application. It contains the business logic that ties all the APIs together and code for generating the Streamlit interface. It also handles the interactions with the web-application, after any button-press, by setting certain values in the `streamlit.session_state` (which is why some of the code is so nested)

- **apis** package - contains all of the code required to interract with the 3rd party API's (StabilityAI, Clarifai and AI21Labs)
- **images** folder - contains sample images for showing in the README
- **response_images** folder - the folder where the StabilityAI images are downloaded, after each app call
- **utils** package - contains different Python functions that are used to process the text response from AI21Labs requests, so that we can later use the text in the app
- [completion_params.json](/apis/ai21labs/completion_params.json) - is a JSON file that is used to store all of the settings for the AI21Labs completion prompt requests that we make to the AI21Labs APIs. We use different settings for different prompts sent to the API, because we have multiple use cases for which we identified different optimal parameter settings.

----

### 💻👨‍💻 Demo

You can try out the application [here](http://34.136.12.178:8501/) (please use HTTP, not HTTPS, because we couldn't use HTTPS because our certificate is not recognized by our browser, because we used a static IP, not a public domain name)

- We have functionality to POST to Twitter, however our application has been closed and is pending approval from Twitter.

#### The logical flow of the application

- Our Streamlit application simulates the way our mobile application would work. 

- Instead of a fridge image generated by Stable Diffusion, you would take a photo of the inside of your fridge and information about the ingredients in the fridge would be extracted.

- Then, from this point forward, the flow of the application would be the same as currently.

- The purpose of clicking each button is to take you to the next step in the "use-case" of the application (ex: generate recipes, generate ingredients required for recipe, generate difference of ingredients between recipe list and existing ingredients etc.)

----

### 🚀 What can this help with?

There are 2 main areas where KitcheGenie can help with. These are, in order of complexity:

- identifying recipes which can be made with already bought ingredients
- identifying ingredients for the recipe (could be more ingredients than you have)
- identifying the "grocery list" with only the extra ingredients, in case your recipe needs a few more items

----

### 💡 Challenges and solutions 🏆

The main way we've used the API's from AI21 Lab were focused more on the Jurrasic1-Instruct model.

We've used Few-Shot Completion model and gave it prompts along with the **Jurassic-1 Instruct** in order to "teach" our model to do some logical operations on the data that we give it, which the model couldn't do by default.

Some of the places we've used this approach are:

- generating a list of ingredients for a selected recipe, in a certain format, to allow for easy processing later on:

    - The default model returned a list of ingredients, sometimes with commas "," for describing the state of the ingredient, like ("onion, chopped"), so that we couldn't easily identify a delimiter between ingredients
    - We've trained the model to return data with ingredients delimited by "||" to allow for easier parsing of ingredients

- comparing the contents of two lists of ingredients

    - We've explored the ability of the Jurassic-1 Instruct model to understand logical operations like difference of sets.
    - We've passed along a "List 1" and "List 2" of ingredients, in text, and trained the model to show us the items that are in "List 2" but not part of "List 1". 
    
        In our application we have used this functionality to automatically determine the ingredients for our shopping list. Although sometimes the model returns items that are in both lists, this is usually rare and happens when comparing longer lists.

        We suggest having a look at the ["demo"](https://www.youtube.com/playlist?list=PLmbqa7kiU8F9fGVrEcKu9NY_RRYbwLHWv) to see how this works.

- generating hashtags that can be used to post a Tweet on Twitter.

    - We've used the same Jurassic-1 Instruct model to make it extract the most important words in a text and return them as hashtags.

All of the settings we used for "training" the model with Few-Shot prompts, for the different scenarios mentioned above, are defined in [`completion_params.json`](apis\ai21labs\completion_params.json)

---

We have also used the Zero-shot Completion and Summarization models to extend our application and enrich the story in our demo.

- We've used the Completion model to recommend recipes based on the ingredients selected in our user interface. Also, we've used this Completion model to let us know what are the ingredients for a selected recipe.

- We've used the Summarization model to do a short summary of our "story" and come up with a short text which can be later shared in a tweet, alongside the suggested hashtags that are returned by our previously mentioned Few-Shot model.

----

### 3rd party API's used

#### Stability AI (Stable Diffusion)
In our application we've also used the Stable Diffusion API from Stability AI to generate images to make our story more immersive. The API generated images of our fridge, like below:

!["fridge1"](images/fridge_1.png)

We've also used the same API to generate images of the grocery shopping:

!["grocery_shopping"](response_images/lamagazin.png)

As well as images of the final cooked recipe:

!["recipe_cooked"](response_images/pasta.png)

#### Clarifai
After generating the image of the interior of the refrigerator, the image is sent to the [Clarifai](https://clarifai.com/) service to identify the ingredients and extract their names.

The names of the ingredients are returned and displayed in the application's multi-select element in the visual interface.

# License

© All rights are reserved and this repository is **NOT** Open Source or Free. You cannot modify or redistribute this code without explicit permission from the copyright holder.
