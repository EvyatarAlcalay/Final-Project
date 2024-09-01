
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

**A list of the main features and functionalities of the project**
- The App is able to take a picture of the wall and a picture of the photo to be hanged ("the photo")
- The App can position the photo anywhere on the wall
- The App can change the photo size
- The App can detect the real photo and direct to hang it

**A list of the main components of the project**
- TakeAPicture.py
- CamScanner.py
- Rotation.py
- HangAPicture.py
- FixPicture.py
- FinalPicture.py
- LivePicture.py

**A list of the main technologies used in the project**\
The App is using with YOLOv8 model to detect the picture when the user hang it.


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
**instructions** 
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

**A step by step series of examples that tell you how to get a development environment running**
- create a folder on the computer pc
- download repository into the folder
- install the packages
- run main.py

## Testing
**Explaination how to run tests for this project**\
we put the camera in distance of 3 and 2 meters from the wall, for each distance in angle of 90 degrees from the wall, 66 degreees an 45 degrees from the wall. we tested 3 times for each combination (distance and angle)

### Test instructions
- run main.py
- Take the picture to be hanged and apporve it
- Crop the picture
- Rotate the picture (if necessary)
- Select the picture of the wall adn approve it
- Crop the picture
- Select a point on the grid to hang the picture
- Fit the size to the real size via the slider
- approve the hanged
- Now a window with the hanged picture on the real wall will be opened. Review and choose other point (if nesessary)
- approve the preview
- follow the guidence to hange the picture


## Built With
  - [Wall Gallery Design Lite App](https://apps.apple.com/il/app/wall-gallery-designer-lite/id1289357200?l=iw) - I took an inspiration for my App from this App
  - [Based on Open CV](https://opencv.org/) - Used for image processing
  - [Understanding Homography](https://towardsdatascience.com/understanding-homography-a-k-a-perspective-transformation-cacaed5ca17) - used to understand how to align a curvate picture
  - [Based on Yolo8v](https://docs.ultralytics.com/models/yolo-world/) - used for detcting the image to be hanged


## Acknowledgments
  - Thank to Gal Katzhendler and Yuri Klebanov which direct me all the way until the app will be perfect
