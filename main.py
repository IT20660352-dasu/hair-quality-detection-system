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
import tempfile



# GitHub repository URL
github_repo_url = "https://github.com/IT20660352-dasu/hair-quality-detection-system"

# Directory to cache downloaded models
cache_dir = "./cached_models"

# Ensure cache directory exists
os.makedirs(cache_dir, exist_ok=True)

# Load models from GitHub URLs
def load_models_from_github():
    models = {}
    for model_file in ['color.h5', 'dandruff.h5', 'Bleached.h5', 'dryness.h5', 'Hair.h5']:
        model_url = f"{github_repo_url}/raw/main/{model_file}"
        response = requests.get(model_url)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.h5') as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        models[model_file.split('.')[0]] = temp_file_path
    return models

# Load models
loaded_models = load_models_from_github()

app = Flask(__name__)

# Route for home page
@app.route('/')
def Home():
    return render_template("home.html")

# Route for step 1
@app.route('/step1', methods=['POST'])
def Hair_step_1():
    return render_template("step1.html")

# Route for step 1 active
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

    # Preprocess the image
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image data

    # Make prediction using model5
    model5_path = loaded_models['Hair']
    model5 = load_model(model5_path)
    prediction5 = model5.predict(img_array)
    threshold = 0.5
    if prediction5[0][0] < threshold:
        classification = "This is Not Hair"
    else:
        classification = "This is hair"

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
    model1_path = loaded_models['color']
    model1 = load_model(model1_path)

    model3_path = loaded_models['Bleached']
    model3 = load_model(model3_path)

    model4_path = loaded_models['dryness']
    model4 = load_model(model4_path)

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
                return jsonify({"prediction": classification, "image_url": img_url})
            else:
                classification = ("Hair is wet")
                os.remove(local_image_path)
                return jsonify({"prediction": classification, "image_url": img_url})
        else:
            classification = ("Bleached Hair ")
            os.remove(local_image_path)
            return jsonify({"prediction": classification, "image_url": img_url})
    else:
        classification = ("Not Black Hair")
        os.remove(local_image_path)
        return jsonify({"prediction": classification, "image_url": img_url})
    
    

    

@app.route('/new', methods=['POST'])
def Hello_word1():
    return  render_template("step2.html")

@app.route('/new2', methods=['POST'])
def Hello_word2():
    return  render_template("step3.html")




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

    model2_path = loaded_models['dandruff']
    model2 = load_model(model2_path)
    prediction2 = model2.predict(img_array)

    threshold = 0.5

    if prediction2[0][0] > threshold:
                classification = ("Danruff hair ")
                os.remove(local_image_path)
                return jsonify({"prediction": classification, "image_url": img_url})
    else:
                classification = ("Not a danruff hair and you can donate your hair")
                os.remove(local_image_path)
                return jsonify({"prediction": classification, "image_url": img_url})

if __name__ == "__main__":
    app.run(port=3000, debug=True,use_reloader=False)
