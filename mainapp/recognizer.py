import base64 as b64
import io

import face_recognition.api as api


# print(dir(fr))

def compare_images2(unknown_image:str, image2:str):
    # image = api.load_image_file(image2)
    # Expecting that both images are base64 strings

    unknown_image = io.BytesIO(b64.b64decode(unknown_image))
    unknown_image = api.load_image_file(unknown_image)
    enc_unknown_image = api.face_encodings(unknown_image)

    image2 = io.BytesIO(b64.b64decode(image2))
    image2 = api.load_image_file(image2)
    enc_image = api.face_encodings(image2)

    if not enc_unknown_image:
        return None
    
    return api.compare_faces([enc_image[0]], enc_unknown_image[0])