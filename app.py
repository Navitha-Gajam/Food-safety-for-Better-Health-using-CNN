import os
import json
import numpy as np
import redis
import tensorflow as tf

from flask import Flask, render_template, request, url_for
from PIL import Image

from tensorflow.keras.applications.vgg16 import preprocess_input as vgg_preprocess
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess


# ---------------- CONFIG ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_SIZE = (224, 224)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- REDIS ----------------

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

print("Redis Keys:", redis_client.keys("*"))


# ---------------- LOAD CLASS INDICES ----------------

with open(os.path.join(BASE_DIR, "class_indices.json"), "r") as f:
    class_indices = json.load(f)

CLASS_NAMES = {v: k for k, v in class_indices.items()}


# ---------------- LOAD MODELS ----------------

MODEL_FILES = {
    "CUSTOM CNN": "custom_cnn.h5",
    "VGG16": "vgg16.h5",
    "RESNET50": "resnet50.h5"
}

MODELS = {}

for name, file in MODEL_FILES.items():

    try:
        path = os.path.join(BASE_DIR, file)

        MODELS[name] = tf.keras.models.load_model(path, compile=False)

        print(f"{name} loaded successfully")

    except Exception as e:
        print(f"{name} failed to load:", e)

print("Loaded Models:", list(MODELS.keys()))


# ---------------- FLASK APP ----------------

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- IMAGE PREPROCESSING ----------------

def preprocess_image(img, model_name):

    img = img.resize(IMG_SIZE)

    img = np.array(img)

    if model_name == "CUSTOM CNN":

        img = np.expand_dims(img, axis=0)

    elif model_name == "VGG16":

        img = vgg_preprocess(img)
        img = np.expand_dims(img, axis=0)

    elif model_name == "RESNET50":

        img = resnet_preprocess(img)
        img = np.expand_dims(img, axis=0)

    return img


# ---------------- REDIS NUTRITION ----------------

def get_food_from_redis(food_name):

    if not food_name:
        return {}

    key = f"food:{food_name.lower()}"

    data = redis_client.get(key)

    if not data:

        return {
            "calories": "N/A",
            "carbs": "N/A",
            "protein": "N/A",
            "fat": "N/A",
            "fiber": "N/A",
            "recommended": "Unknown"
        }

    raw = json.loads(data)

    return {

        "calories": raw.get("calories_kcal", "N/A"),
        "carbs": raw.get("total_carbohydrates_g", "N/A"),
        "protein": raw.get("protein_g", "N/A"),
        "fat": raw.get("fat_g", "N/A"),
        "fiber": raw.get("fiber_g", "N/A"),
        "recommended": "Yes" if raw.get("category") == "veg" else "No"

    }


# ---------------- MODEL METRICS FROM REDIS ----------------

def load_metrics(key):

    data = redis_client.get(key)

    if not data:
        return None

    metrics = json.loads(data)

    precision = recall = f1 = "N/A"

    cr = metrics.get("classification_report")

    if isinstance(cr, dict) and "weighted avg" in cr:

        precision = cr["weighted avg"].get("precision", "N/A")
        recall = cr["weighted avg"].get("recall", "N/A")
        f1 = cr["weighted avg"].get("f1-score", "N/A")

    return {

        "train_accuracy": metrics.get("train_accuracy", 0),
        "val_accuracy": metrics.get("val_accuracy", 0),
        "test_accuracy": metrics.get("test_accuracy", 0),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "classification_report": cr

    }


cnn_metrics = load_metrics("model:cnn:metrics")
vgg_metrics = load_metrics("model:vgg16:metrics")
resnet_metrics = load_metrics("model:resnet50:metrics")


# ---------------- ROUTE ----------------

@app.route("/", methods=["GET", "POST"])
def index():

    predicted_class = None
    confidence = None
    nutrition = {}
    recommended = None
    filename = None
    model_selected = None
    metrics = None
    show_result = False

    if request.method == "POST":

        file = request.files.get("image")
        model_selected = request.form.get("model")

        if file and model_selected in MODELS:

            filename = str(np.random.randint(1000000)) + "_" + file.filename

            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(save_path)

            img = Image.open(save_path).convert("RGB")

            image_array = preprocess_image(img, model_selected)

            model = MODELS[model_selected]

            predictions = model.predict(image_array)

            print("Prediction vector:", predictions)

            predicted_index = int(np.argmax(predictions[0]))

            predicted_class = CLASS_NAMES.get(predicted_index, "Unknown")

            confidence = round(float(np.max(predictions)) * 100, 2)

            print("Predicted class:", predicted_class)

            nutrition = get_food_from_redis(predicted_class)

            recommended = nutrition.get("recommended", "Unknown")

            if model_selected == "CUSTOM CNN":
                metrics = cnn_metrics

            elif model_selected == "VGG16":
                metrics = vgg_metrics

            elif model_selected == "RESNET50":
                metrics = resnet_metrics

            show_result = True

    return render_template(

        "index.html",

        available_models=list(MODELS.keys()),

        model_selected=model_selected,

        show_result=show_result,

        predicted_class=predicted_class,

        confidence=confidence,

        nutrition=nutrition,

        recommended=recommended,

        filename=filename,

        image_url=url_for("static", filename="uploads/" + filename) if filename else None,

        train_accuracy=metrics["train_accuracy"] if metrics else "N/A",

        val_accuracy=metrics["val_accuracy"] if metrics else "N/A",

        test_accuracy=metrics["test_accuracy"] if metrics else "N/A",

        precision=metrics["precision"] if metrics else "N/A",

        recall=metrics["recall"] if metrics else "N/A",

        f1_score=metrics["f1"] if metrics else "N/A",

        classification_report=metrics["classification_report"] if metrics else ""

    )


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
'''from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import os
import json
import redis
from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg_preprocess
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess

app = Flask(__name__)

# Redis Connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Load ModelsUnresolved reference 'class_names'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS = {
    "CUSTOM CNN": tf.keras.models.load_model(os.path.join(BASE_DIR, "custom_cnn.h5")),
    "VGG16": tf.keras.models.load_model(os.path.join(BASE_DIR, "vgg16.h5")),
    "RESNET50": tf.keras.models.load_model(os.path.join(BASE_DIR, "resnet50.h5")),
}

IMG_SIZE = (224, 224)

# Load class names from Redis (example from best model)
resnet_data = json.loads(r.get("resnet50_results"))
CLASS_NAMES = list(resnet_data["classification_report"].keys())
CLASS_NAMES = [c for c in CLASS_NAMES if c not in ["accuracy", "macro avg", "weighted avg"]]


def preprocess_image(image):
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


@app.route("/")
def home():
    return render_template("index.html", classes=CLASS_NAMES)


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    model_name = request.form["model"]

    model = MODELS[model_name]

    # Open image correctly
    image = Image.open(file.stream).convert("RGB")
    image_array = preprocess_image(image)

    # Resize to model input size
    #image = image.resize((224, 224))

    # Convert to array

    #image_array = np.array(image) / 255.0
    #image_array = np.expand_dims(image_array, axis=0)

    # Predict
    predictions = model.predict(image_array)
    predicted_index = int(np.argmax(predictions))
    predicted_class = CLASS_NAMES[predicted_index]

    # Fetch model metrics from Redis
    redis_key = f"{model_name.lower().replace(' ', '_')}_results"
    redis_data = json.loads(r.get(redis_key))
    print("Model Selected:", model_name)
    print("Test Accuracy:", redis_data["test_accuracy"])

    # Filter only selected class metrics
    class_metrics = redis_data["classification_report"][predicted_class]

    # Fetch nutrition data from Redis
    nutrition_data = r.get(predicted_class.lower())

    if nutrition_data:
        nutrition_data = json.loads(nutrition_data)
    else:
        nutrition_data = {"message": "No nutrition data available"}

    return jsonify({
        "predicted_class": predicted_class,
        "test_accuracy": float(redis_data["test_accuracy"]),
        "classification_report": redis_data["classification_report"],
        "nutrition": nutrition_data
    })


if __name__ == "__main__":
    app.run(debug=True)'''
