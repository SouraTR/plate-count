# plate-count
Counts number of colonies in a petri plate

Using opencv library I managed to count numbers of colonies in a petri plate
Get the number of colonies as the shape of "detected_circles" numpy array

Code needs a lot of optimization and automation

# Current Goals

  1. Automatically reduce resolution of picture and crop to 500x500 at 72dpi
  2. Put a solid color matte around the plate to avoid miscounting
 
# Libraries
  skimage
  matplotlib
  numpy
  open-cv
  
# References
  1. https://www.geeksforgeeks.org/circle-detection-using-opencv-python/
