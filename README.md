
# 💡 Image On a Wall – Layout Planner
<!-- cool project cover image -->
![Project Cover Image](/assets/opening_pic.jpg)

<!-- table of content -->
## Table of Contents
- [The Team](#The-Team)
- [Project Description](#Project-Description)
- [Getting Started](#Getting-Started)
- [Prerequisites](#Prerequisites)
- [Installing](#Installing)
- [Testing](#Testing)
- [Deployment](#Deployment)
- [Built With](#Built-with)
- [Acknowledgments](#Acknowledgments)

## The Team 
**Team Members**
- [Evyatar Alcalay](evyataralcalay@mail.huji.ac.il)

**Supervisor**
- [Gal Katzhendler](gal.katzhendler@mail.huji.ac.il)


## Project Description 
**A brief description of the project/challange, what it does, and how it works**\
The Layout Planner App helps users to hang easily a picture on a wall without using any measurement tools. 
Existing Apps only provide illustration of how the picture will be appeared on the wall while the Layout Planner provides the user voice guidance (by Text to speech) and text guidance of how and where to hang the picture in wall according to the user preference and symmetrically to the wall.

- A list of the main features and functionalities of the project.
- A list of the main components of the project.
- A list of the main technologies used in the project.


## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. 

### Prerequisites
Requirements for the software and other tools to build, test and push 
- camera (internal or external, now the project work on external camera nut you can change to work with the computer camera by replace)
- rectangular and smooth wall (its not prommised the app will work on other walls)  
- rectangular picture
- internet connection
- speakers (to hear the voice guidence)

### Installing
**instructions**\
- First, you have to install python 3.11.7
- Second, you have to install visual studio code
- Third, you have to install all of these packages:
  * pillow (PIL)
  * cv2
  * numpy
  * matplotlib
  * torch
  * ultralytics
  * playsound
  * gtts
- Also, the app is used with the built in packages (verify you have them)
  * math
  * tkinter
  * os.path
  * os
  * threading
  * time

**A step by step series of examples that tell you how to get a development environment running**\
- create a folder on the computer pc
- download repository into the folder
- install the packages
- run main.py

## Testing
**Explaination how to run tests for this project**\
we put the camera in distance of 3 and 2 meters from the wall, for each distance in angle of 90 degrees from the wall, 66 degreees an 45 degrees from the wall. we tested 3 times for each combination (distance and angle)

### Sample Tests
Explain what these tests test and why

    Give an example

## Deployment
Add additional notes on how to deploy this on a live system

## ⚙️ Built With
  - [Based on the amazing work of reserch group xxxx](https://www.example.com)
  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used for the Code of Conduct
  - [Creative Commons](https://creativecommons.org/) - Used to choose the license


## Acknowledgments
  - Hat tip to anyone whose code is used
  - Inspiration
  - etc
