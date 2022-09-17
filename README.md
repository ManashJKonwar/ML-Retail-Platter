# Retail Pricing Simulator
> Retail Pricing Simulator is developed so that business scenarios or decisions made across pricing of products could be easily rendered and visualized, thereby enabling users to simulate real time scenarios and leverage the power of ML to forecast the demand in near future.

> Live demo [_here_](https://www.example.com). <!-- If you have the project hosted somewhere, include the link here. -->

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Dataset Utilized](#dataset-utilized)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [References](#references)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->

## General Information
- The aim of this repository is to help AI/ML researchers develop historical dashboarding for retail data and also generate an inferencing simulator which would connect directly to databases and deployed models to generate demands.
- Another selling point is the utilization of DASH which is a python framework running Flask as web server, React JS as frontend and Plotly JS as visualization modules.

![Retail Simulator Architecture](./repo_assets/Retail_Simulator_Architecture.jpg)

- Please do refer to the Learn More Sections in each page of the web application to deep dive into each of this case studies.

## Technologies Used
- Tensorflow2
- Keras
- Dash 

## Features
List the ready features here:
- Training and Inferencing Pointnet Classifier - Done
- Training and Inferencing Pointnet Part Segmenter - Done
- Training and Inferencing Pointnet Semantic Segmenter - To Be Started

## Screenshots
![Pointnet Classifier Frontend](./repo_assets/Pointnet_Classifier_Frontend.jpeg)
![Pointnet Part Segmenter Frontend](./repo_assets/Pointnet_Part_Segmenter_Frontend.jpeg)

## Setup:
- git clone https://github.com/ManashJKonwar/IP-Pointnet.git (Clone the repository)
- python3 -m venv IPPointnetVenv (Create virtual environment from existing python3)
- activate the "IPPointnetVenv" (Activating the virtual environment)
- pip install -r requirements.txt (Install all required python modules)

## Dataset Utilized:
- [PointNet Classifier](http://3dvision.princeton.edu/projects/2014/3DShapeNets/)
Credit goes to [ModelNet 10 dataset](http://modelnet.cs.princeton.edu/) which contains CAD Models from 10 common categories. This is actually a subset of ModelNet 40 dataset.
Each of the point under each object category consist of labelling as to which object category it belongs and this information helps us greatly to perform training as well as validation 
runs.
- [Pointnet Part Segmenter](http://3dvision.princeton.edu/projects/2014/3DShapeNets/)
Credit goes to [ShapeNet dataset](https://shapenet.org/). Its an ongoing effort to establish a richly-annotated, large-scale dataset of 3D shapes. ShapeNetCore is a subset of the 
full ShapeNet dataset with clean single 3D models and manually verified category and alignment annotations. It covers 55 common object categories, with about 51,300 unique 3D models.
I have utilized only 12 object categories of PASCAL 3D+, included as part of the ShapenetCore dataset and each of this category contains part level labelling for perform training as 
well as validation runs


## Usage
### For Training PointNet:
- python train_pointnet.py
### For Running Web Application:
- python index.py

## Project Status
Project is: __in progress_ 
<!-- / _complete_ / _no longer being worked on_. If you are no longer working on it, provide reasons why._ -->

## Room for Improvement
Room for improvement:
- Build a generic classifier for custom 3d dataset
- Build a generic part segmenter for custom 3d dataset
- Build a generic semantic segmenter for custom 3d dataset
- Develop frontend to encompass this generic nature
- Porvide support for CPUs, GPUs and TPUs as well

To do:
- Finish developing inference end of part segmenter at DASH end
- Start developing semantic segmenter

## References
[1] PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation; Charles R. Qi, Hao Su, Kaichun Mo, Leonidas J. Guibas;
CVPR 2017; https://arxiv.org/abs/1612.00593.

## Acknowledgements
- This project was based on [Point cloud classification with PointNet](https://keras.io/examples/vision/pointnet/).
- This project was based on [Point cloud segmentation with PointNet](https://keras.io/examples/vision/pointnet_segmentation/).

## Contact
Created by [@ManashJKonwar](https://github.com/ManashJKonwar) - feel free to contact me!

Optional -->
## License
This project is open source and available under the [... License]().

<!-- You don't have to include all sections - just the one's relevant to your project -->