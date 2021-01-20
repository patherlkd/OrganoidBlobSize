# OrganoidBlobSize
A python toolkit to generate simple workflows to extract features in images generated using AFM e.g.

(This was done as an extra-curricular venture, **this works as is**. Please do play around with the blob criteria to further "refine" the areas.)

## System Requirements

This code relies only on python3. Please install python3 (free) on your system (Windows, Linux, Mac). The code was tested on Ubuntu linux 18 LTS.

## How to use the script

First we need images. Place your organoid blob images in the folder ``images``. Ensure that each image is as you would expect and they all share the same area per pixel (and ideally size).

An image could look like:

![organoid](organoid_example.png)


## Example_workflow.py

The main code for this problem, to refine the areas you only need to edit this code.


# Supporting and other useful codes

These codes should be present in the same folder as ``Example_workflow.py`` but, if you don't know what you are doing, you shouldn't edit them.

## py_image_LD.py 

Main supporting code. Contains functions to manipulate and probe the images.

## cluster.py

Contains the functions to cluster and segment objects, could be useful for further enhancements/problems.
