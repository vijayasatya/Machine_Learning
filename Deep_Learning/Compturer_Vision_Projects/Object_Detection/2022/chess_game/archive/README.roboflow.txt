
Chess Pieces - v24 416x416_aug
==============================

This dataset was exported via roboflow.ai on February 23, 2021 at 5:33 PM GMT

It includes 693 images.
Pieces are annotated in YOLO v5 PyTorch format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 416x416 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* Randomly crop between 0 and 15 percent of the image
* Random shear of between -6° to +6° horizontally and -6° to +6° vertically
* Random brigthness adjustment of between -10 and +10 percent
* Random exposure adjustment of between -10 and +10 percent


