QC scripts:
Overall, these scripts determine how much data loss there is due to our FOV sometimes not being optimized to cover the whole brain for some individuals. 

The script determines how much of each ROI comprising the intrinsic connectome, defined by the atlas, we have in our data. 

For spheres that are not covered well-enough (which we define as have less than 80% of the voxels we should expect in Standard Space),
we output a .csv file describing which subject, which ROI, and what percentage of the sphere we have in our data.
