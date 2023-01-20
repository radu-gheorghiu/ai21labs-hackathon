from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


USER_ID = "<YOUR USER ID>"
PAT = "<ADD YOUR KEY HERE>"
APP_ID = "<YOUR APP_ID>"
MODEL_ID = "<YOUR FOOD MODEL ID>"
MODEL_VERSION_ID = ""
CONFIDENCE_THRESHOLD = 0.65
MAX_CONCEPTS = 15
BLACKLIST = [
    "vegetable",
    "aliment",
    "legume",
    "fruit",
    "micronutrient",
    "collation",
    "pasture",
    "herb",
    "platter",
    "feast",
]


class Clarifai:
    def __init__(self):
        channel = ClarifaiChannel.get_grpc_channel()
        self._stub = service_pb2_grpc.V2Stub(channel)
        self._metadata = (("authorization", "Key " + PAT),)
        self._userDataObject = resources_pb2.UserAppIDSet(
            user_id=USER_ID, app_id=APP_ID
        )

    def __call__(self, image_path):
        with open(image_path, "rb") as f:
            file_bytes = f.read()
        image_obj = resources_pb2.Input(
            data=resources_pb2.Data(image=resources_pb2.Image(base64=file_bytes))
        )
        request_signature = self._prepare_request(image_obj)
        response = self._stub.PostModelOutputs(
            request_signature, metadata=self._metadata
        )
        if response.status.code != status_code_pb2.SUCCESS:
            print(response.status)
            raise Exception(
                f"Image captions generation failed, status: {response.status.description}"
            )

        concepts = [
            concept.name
            for concept in response.outputs[0].data.concepts
            if float(concept.value) >= CONFIDENCE_THRESHOLD
            and concept.name not in BLACKLIST
        ][:MAX_CONCEPTS]
        return concepts

    def _prepare_request(self, img_object):
        return service_pb2.PostModelOutputsRequest(
            user_app_id=self._userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[img_object],
        )


def main():
    clarifai = Clarifai()
    print("Predicted concepts:")
    print(clarifai("food2.png"))
