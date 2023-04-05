# Investigating-machine-learning-for-simulating-urban-transport-patterns
A Comparative analysis for Machine learning vs Traditional Gravity Model

This repository contains the code for a research paper on a comprehensive transport model for trip predictions. The research investigates the data requirements for trips at the city level with considerable diversity and compares simulations based on SIM and Machine Learning models.

Research Description
The full research paper can be found here. The research focuses on developing a machine learning model for predicting trip patterns in urban areas, based on various factors such as time of day, day of the week, weather conditions, and more. The model uses data from trip logs provided by Telia company, which has been anonymized to protect privacy.

The research also includes network analysis to calculate the shortest distance between all urban districts, which is used for further analysis in the spatial interaction model (SIM) as well as the machine learning model for the parameter calculations of cost of transport. The spatial interaction model is developed based on Wilson's ideology of Gravity theory.

The interactive dashboard is available over the hosted platform pythonanywhere, powered specifically for python web applications. The programming in python is based on Dash and uses IBM Watson (Cloud Technology) as a backend where the machine learning model is deployed. The SHAP analysis for the XGBoost regression model is included in the Google Colab notebook.

Interactive Dashboard and Backend Programming
The interactive dashboard is available over the hosted platform pythonanywhere (figure A.0.1), powered specifically for python web applications. The programming in python is based on Dash and uses IBM Watson (Cloud Technology) as a backend where the ML model is deployed. The files and code are available over the web interface here: TransportModelApp.

Network Analysis
The network analysis is based on the OSM files invoked over the python notebook. The shortest path algorithm gives the shortest distance between all the Urban Districts. This distance is used for further analysis in the SIM as well as the machine learning model for the parameter calculations of cost of transport. The code for the shortest path can be accessed over IBM Watson notebook here: ShortestDistance.

Spatial Interaction Model
The spatial interaction model (SIM) is hosted over a notebook in IBM Watson console for obtaining predictions. The family of SIM is developed based on Wilson's ideology of Gravity theory. It can be accessed here: GravityModel.

Machine Learning Model
Various machine learning algorithms were tried for best fit. The Extreme Gradient Boost (XGB) algorithm gives the best fit for available 2019 data. Sensitivity analysis was used to prioritize and select the most efficient parameters for the model. The developed machine learning model can be accessed similarly here: XGBmodel.

The machine learning model is deployed in the backend over IBM Watson. The deployed model consumes for the configuration at an average 2.5 Capacity Unit Hour (CUH) for every run of the analysis. Even with a low processing capacity, the model has a relatively fast processing for analysis.

It is possible to develop the model by providing the ability of uploading the parameters and invoking the road network over OSM or Mapbox GL JS (for faster and more accurate analytical ability of cost of transport including the waiting times). Using GPU (TensorFlow) would optimize the model execution time further, when we use real-time data, depending on the matrix size.

The SHAP analysis for the XGBoost regression model is included in the Google Colab notebook.

Code
The code included in this repository is written in Python and consists of the following files:


Usage
To use the code, you need to have Python 3 and the required libraries installed. You can run the simulations by executing the simulation.py file, and the visualization code is available in the visualization.py file.

Contribution
Contributions to the code are welcome. If you have any questions or suggestions, please open an issue in the repository.

Confidentiality Note
The trip data was acquired by WSP Sweden from Telia company and has been used for this research in confidentiality. It can be made available upon request and proper confidentiality agreement with Telia and WSP Sweden organization.
