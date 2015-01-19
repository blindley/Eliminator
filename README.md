Eliminator
==========

A simple program which allows you to select the best image (for whatever purpose) from an arbitrarily sized directory of images.

## Usage

Create a directory, and place a bunch of image files in it. Then run the program from that directory. You will be presented with two of the images, selected at random (or using some yet to be determined formula). Just click the image which you prefer. Repeat. You may close the program any time. When you start it up again, you will continue your progress.

When you first start the program in a particular directory, a sub-directory named "eliminator_data/" will be created with a file "data.txt".  You can see the status of the selection process in this file. The image file names are in order of points, with the most frequently selected image at the top.

## Use case

Let's say you want to select a profile picture for Facebook, or some other social media. You have hundreds of pictures, and you want to select the best looking one. Selecting the best out of hundreds of options is a difficult, and possibly stressful task. However, when you only have 2 choices, it is much simpler to compare them, and select a winner. Kind of like a tournament, which is decided by a sequence of games between 2 teams. Eventually, one of the teams rises to the top, by whatever mechanism the particular tournament system determines scoring.

## Future plans

* Support more than just images. Pieces of text, as well as video and music clips.
* Give the user an option of what kind of tournament system to use *(elimination, round-robin, etc...)*
