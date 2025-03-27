### This directory stores the UCF-101 dataset. The descriptions of the folders are as follows:

**annotations** --stores the labels for training and testing of the dataset.

**videos**--stores the original video.


**rawframes_flow**--stores stacked optical flow rawframes.

**rawframes_rgb+flow**--stores RGB frames and optical flow images, of which 50% are optical flow images.

**rawframes_rgb+flow_sparse**--stores RGB frames and optical flow images, of which 67% are optical flow images.

**rawframes_concat**--stores the rawframes of the optical flow and the RGB head-to-tail stitching.

**ucf101_train/val_split_1/2/3_rgb+XXX.txt**--training/testing split for different sparse sampling methods.
