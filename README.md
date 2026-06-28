Food Safety for Better Health using CNN
Deep Learning Based Food Classification and Nutritional Analysis System
Author: Navitha G

Project Overview

Food Safety for Better Health using CNN is a deep learning-based web application that classifies food images and provides nutritional information to promote healthier eating habits. The system compares Custom CNN, VGG16, and ResNet50. After prediction, it retrieves nutritional facts, model metrics, and classification reports from Redis and displays them in a Flask web interface.


Objectives

•	Classify food images using Deep Learning.

•	Compare three CNN models.

•	Display model performance.

•	Retrieve nutritional facts from Redis.

•	Build an interactive Flask web application.


Features

•	Upload food image.

•	Select prediction model (Custom CNN, VGG16, ResNet50).

•	Display uploaded image.

•	Display predicted food image/class.

•	Show prediction confidence.

•	Display nutritional facts.

•	Show Healthy/Unhealthy badge.

•	Display Test Accuracy, Precision, Recall, F1 Score, Classification Report.

•	Retrieve model metrics from Redis.

•	Modern responsive UI.



Technologies Used

•	Python 3.10

•	TensorFlow

•	Keras


•	NumPy

•	OpenCV

•	Pillow

•	Flask

•	Redis

•	HTML5

•	CSS3

•	JavaScript


Project Structure
Food Safety For Better Health Using CNN/
├── app.py
├── custom_cnn.h5
├── vgg16.h5
├── resnet50.h5
├── templates/index.html
├── static/profile.jpg
├── static/uploads/
├── dataset/
├── redis/
└── requirements.txt


Dataset
34 food classes including Apple Pie, Burger, Pizza, Taco, Sandwich, Idli, Dhokla, Jalebi, Paani Puri, Kulfi, Momos, Sushi, Butter Naan, Kadai Paneer, Chole Bhature, Pav Bhaji and more.


Deep Learning Models

1. Custom CNN (~13.8% accuracy)
2. VGG16 (~64.7% accuracy)
3. ResNet50 (~77.35% accuracy)


Redis Database

•	Nutritional Facts: Calories, Protein, Fat, Carbohydrates, Fiber, Healthy/Unhealthy Category.

•	Model Metrics: Test Accuracy, Precision, Recall, F1 Score, Classification Report.



Workflow

•	Upload image.

•	Select model.

•	Flask preprocesses image.

•	Model predicts class.

•	Retrieve Redis data.

•	Display results.


User Interface

•	Left Panel: Profile Photo, Author Details, Skills.

•	Center Panel: Upload Image, Predicted Image, Model Selection, Predict Button.

•	Right Panel: Food Classes, Predicted Food, Badge, Nutritional Facts, Test Accuracy, Classification Report.


Installation

pip install -r requirements.txt

redis-server

python app.py

Open: http://127.0.0.1:5000
