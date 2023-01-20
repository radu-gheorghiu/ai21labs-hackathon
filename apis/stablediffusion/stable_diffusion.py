import os
import io
import warnings
import random
import datetime

# from k2keys.key_reader import key_reader
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

os.environ["STABILITY_HOST"] = "grpc.stability.ai:443"
os.environ["STABILITY_KEY"] = "<YOUR STABILITY KEY HERE>"


class StableDiffussion:
    """The StableDifussion class is used to handle all operations regarding the"""

    _stability_api = None
    _answers = None

    def __init__(self):
        self._create_connection()

    def __call__(self, prompt):
        if len(os.listdir("response_images")) > 100:
            random_img = random.randint(0, len(os.listdir("response_images")) - 1)
            image_file_path = (
                "response_images/" + os.listdir("response_images")[random_img]
            )
        else:
            self._generate_prompt_image(prompt)
            image_file_path = self._save_prompt_image()
        return image_file_path

    def _create_connection(self):
        # Set up our connection to the API.
        self._stability_api = client.StabilityInference(
            key=os.environ["STABILITY_KEY"],  # API Key reference.
            verbose=True,  # Print debug messages.
            engine="stable-diffusion-v1-5",  # Set the engine to use for generation.
            # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
            # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
        )

    def _generate_prompt_image(self, prompt):
        seed = random.randint(1751497630, 1771497630)
        self._answers = self._stability_api.generate(
            prompt=prompt,
            seed=seed,
            steps=88,
            cfg_scale=14,
            width=704,
            height=704,
            samples=1,
            sampler=generation.SAMPLER_K_DPM_2_ANCESTRAL,
            # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
            guidance_preset=generation.GUIDANCE_PRESET_FAST_GREEN,
        )

    def _save_prompt_image(self):
        # Set up our warning to print to the console if the adult content classifier is tripped.
        # If adult content classifier is not tripped, save generated images.
        for resp in self._answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again."
                    )
                elif artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    img_filepath = (
                        "response_images/"
                        + str(artifact.seed)
                        + f"{str(datetime.datetime.utcnow()).replace(':', '_').replace(' ', '-')}.png"
                    )
                    img.save(
                        img_filepath
                    )  # Save our generated images with their seed number as the filename.
                return img_filepath


def main():
    sd = StableDiffussion()
    image_file_path = sd(
        "A very realistic image of the inside a fridge, with different food items, vegetables, dairy and meats, a large variety"
    )
    print(image_file_path)


if __name__ == "__main__":
    main()
