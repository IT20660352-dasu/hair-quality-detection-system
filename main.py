from flask import Flask , render_template ,request ,jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import load_model
import os
from tensorflow.keras.preprocessing import image
import cloudinary.uploader
from PIL import Image
from io import BytesIO
import requests

model1 = load_model(os.path.join('D:/HairDonation/Models','color.h5'))
model2 = load_model(os.path.join('D:/HairDonation/Models','dandruff.h5'))
model3 = load_model(os.path.join('D:/HairDonation/Models','Bleached.h5'))
model4 = load_model(os.path.join('D:/HairDonation/Models','dryness.h5'))
model5 = load_model(os.path.join('D:/HairDonation/Models','Hair.h5'))
app = Flask(__name__)



@app.route('/')
def Home():
    return  render_template("home.html")  #hair_home.jsx

@app.route('/step1', methods=['POST'])
def Hair_step_1():
    return  render_template("step1.html") #hairSampleUpload1.jsx

@app.route('/step1_active', methods=['POST'])
def Hair_step_2():
    imagefile = request.files["imagefile"]

    # Upload image to Cloudinary without saving locally
    cloudinary.config(
        cloud_name="dirwtcy3z",
        api_key="485415999557293",
        api_secret="uEToBNfhveNQGUvZNQ8LmUOngUg"
    )
    upload_result = cloudinary.uploader.upload(imagefile, folder="hair_classification")

    img_url = upload_result["secure_url"]

    # Download the image from the URL
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((150, 150))  # Resize the image to the target size

    # Save the image locally
    local_image_path = "./temp_image.jpg"
    img.save(local_image_path)

    # Load the saved image using PIL
    img = Image.open(local_image_path)

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image data

    prediction5 = model5.predict(img_array)

    threshold = 0.5

    if prediction5[0][0] < threshold:
        classification = "This is Not Hair" #donateReject.jsx
    else:
        classification = "This is hair" #hairOutput1.jsx

    # Delete the temporarily saved image
    os.remove(local_image_path)

    return jsonify({"prediction": classification, "image_url": img_url})

    
@app.route('/step2_active', methods=['POST'])
def Hair_step_3():
    imagefile = request.files["imagefile"]
 # Upload image to Cloudinary without saving locally
    cloudinary.config(
        cloud_name="dirwtcy3z",
        api_key="485415999557293",
        api_secret="uEToBNfhveNQGUvZNQ8LmUOngUg"
    )
    upload_result = cloudinary.uploader.upload(imagefile, folder="hair_classification")

    img_url = upload_result["secure_url"]

    # Download the image from the URL
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((150, 150))  # Resize the image to the target size

    # Save the image locally
    local_image_path = "./temp_image.jpg"
    img.save(local_image_path)

    # Load the saved image using PIL
    img = Image.open(local_image_path)

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image data
    prediction1 = model1.predict(img_array)
    prediction3 = model3.predict(img_array)
    prediction4 = model4.predict(img_array)
 

    threshold = 0.5
    if prediction1[0][0] > threshold:
        classification = ("Black Hair ")
        if prediction3[0][0] < threshold:
            classification = ("Black Hair And Not Bleach Hair ")
            if prediction4[0][0] > threshold:
                classification = ("Black Hair And Not Bleach Hair And Dry Hair")
                os.remove(local_image_path)
                return jsonify({"prediction": classification, "image_url": img_url}) #hairOutput2.jsx
            else:
                classification = ("Hair is wet")
                os.remove(local_image_path)
                return jsonify({"prediction": classification, "image_url": img_url})#donateReject.jsx
        else:
            classification = ("Bleached Hair ")
            os.remove(local_image_path)
            return jsonify({"prediction": classification, "image_url": img_url})#donateReject.jsx
    else:
        classification = ("Not Black Hair")
        os.remove(local_image_path)
        return jsonify({"prediction": classification, "image_url": img_url})#donateReject.jsx
    
    



@app.route('/danruff_upload', methods=['POST'])
def Hello_word3():
    imagefile = request.files["imagefile"]
    # Upload image to Cloudinary without saving locally
    cloudinary.config(
        cloud_name="dirwtcy3z",
        api_key="485415999557293",
        api_secret="uEToBNfhveNQGUvZNQ8LmUOngUg"
    )
    upload_result = cloudinary.uploader.upload(imagefile, folder="hair_classification")

    img_url = upload_result["secure_url"]

    # Download the image from the URL
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((150, 150))  # Resize the image to the target size

    # Save the image locally
    local_image_path = "./temp_image.jpg"
    img.save(local_image_path)

    # Load the saved image using PIL
    img = Image.open(local_image_path)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image data

    prediction2 = model2.predict(img_array)

    threshold = 0.5

    if prediction2[0][0] > threshold:
                classification = ("Danruff hair ")
                os.remove(local_image_path)
                return jsonify({"prediction": classification, "image_url": img_url})#donateReject.jsx
    else:
                classification = ("Not a danruff hair and you can donate your hair") #thankyou.jsx
                os.remove(local_image_path)
                return jsonify({"prediction": classification, "image_url": img_url})

if __name__ =="__main__":
    app.run(port =3000,debug=True)