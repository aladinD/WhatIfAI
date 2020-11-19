<div align="center">

# README - What If AI

![alt text](/documentation/misc/img/logo.png "WhatIfAI")



README for group 11 of the 2020 Applied Machine Intelligence lecture at TUM. 
</div>

## Table of contents

- [README - What If AI](#readme---what-if-ai)
  * [Table of contents](#table-of-contents)
  * [Short project description](#short-project-description)
  * [Requirements](#requirements)
  * [How to use](#how-to-use)
  * [File structure](#file-structure)
    + [Data sets](#data-sets)
    + [Documentation](#documentation)
    + [Code base](#code-base)
    + [Model Parameters](#model-parameters)
  * [Project members](#project-members)
  * [Video](#video)

## Short project description
This project aims to quantify the impact that the Covid-19 pandemic has on the global economy, utilising machine learning. One of the main limitations in machine learning is the modelling of unsampled regions in the feature space. Furthermore, models learned during the training process are only valid in the context of unchanged underlying data generation processes. Since the Covid-19 pandemic fundamentally changed the way our society operates, and we don't have any samples of a global pandemic of smaller and/or greater size, it is impossible to directly model the impact of the virus on different branches of the economy. Instead, we aim to model the economy without the pandemic ensuing from January 2020 on. The impact of the pandemic can then be measured as the difference of the predicted courses without Covid-19, and the actual, observed outcomes. The models and its predictions are made accessible with an interactive web interface.


## Requirements

In order to run the project, you need to have Docker and docker-compose installed on your machine. Running the project with Docker takes care of installing the correct project dependencies and environments. 

## How to use

After cloning the directory, you can start the project by running the [docker-compose](/docker-compose.yml) file. This starts both the front- and the backend of our web server. Both docker containers for the front- and backend will build and start up automatically. You can now access the webpage using any browser of your liking at http://localhost:8080/#/.

> **_NOTE:_** Start the docker-compose from the root directory of the project using:
> ```sh
> <user>:~$ docker-compose up
> ```

> **_WARNING:_** Building the docker image for the first time takes a lot of time. Some installation steps are complex, and the libraries are quite large. Even if the installation seems to stop, be patient.

## File structure

### Data sets
All data sets can be found in the [res](/res) folder. Most Subsets have their own README explaining particular details for this individual set such as the location of related code or comments on the quality.  

> **_NOTE:_** Not all data sets were used in the final project.

### Documentation

The project documentation can be found in the [documentation](/documentation) folder. The project's code is documented with Doxygen. To access the documentation, simply open the [index](/documentation/html/index.html) file with a web browser of your liking. The documentation folder also includes all [milestone reports](/documentation/reports) as well as some meeting transcripts. The final report is located [here](/documentation/reports/milestone_4_report.pdf).

### Code base

Our code base is located in the [src](/src) folder. Scrapers, API scripts etc. to obtain raw data can be found in the [data_collection](/src/data_collection) folder. Basic preprocessing and data extraction scripts are located in [data_management](/src/data_management). The unified data preprocessing scripts are saved in [data_pipeline](/src/data_pipeline). The code for training, final model evaluation and live inference for the web interface is located in [inference](/src/inference). Finally, [webinterface](/src/webinterface) contains the code for both front- and backend. As mentioned before, a complete documentation of the code can be accessed by opening the [Doxygen documentation](/documentation/html/index.html) in a web browser.

### Model Parameters

The model parameters were determined by cross validation. We created a dictionary with the optimal parameters in our [model file](src/inference/prophet.py). Using the parameters, the model is trained on the respective time series.

## Project members

- Aladin Djuhera
- Martin Schuck
- Niklas Landerer
- Michael Brandner
- Felix Montnacher
- Henrique Soares Frutuoso
- Alexander Griessel
- Aron Endres
- Maximilian Putz

## Video 

<div align="center">
      <a href="https://www.youtube.com/watch?v=AChsZ0fCOjk&feature=youtu.be">
     <img 
      src="https://img.youtube.com/vi/AChsZ0fCOjk/0.jpg" 
      alt="what_if.ai" 
      style="width:100%;">
      </a>
    </div>
