# AMT_Real_vs_Fake

Run "real vs fake" experiments on Amazon Mechanical Turk (AMT).

## Synopsis
Runs a series "real vs fake" trials. Each trial pits a real image against a "fake" image generated by an algorithm.

## Requirements
Python

## Usage
- Put all images to test in a web accessible folder. This folder should have subfolders for the results of each algorithm you would like to test (names of subfolders are specified in `opt.which_algs_paths`). Must also contain a subfolder for the real images (path: `opt['gt_path']`). Images should be named "0.jpg", "1.jpg", etc, in consecutive order up to some total number of images N (or they can be named differently, but you will have to specify a lambda function in `opt['filename']`).
- Set experiment parameters by modifying `opt` in `getOpts` function.
- Run `python mk_expt.py -n EXPT_NAME` to generate data csv and index.html for Turk.
- Create experiment using AMT website or command line tools. For the former option, paste contents of index.html into HIT html code. Upload HIT data from the generated csv.
- After collecting results, run `python process_csv.py -f CSV_FILENAME --N_imgs NUMBER_IMAGES --N_practice NUMBER_PRACTICE`. This will compute and run bootstrap statistics.

## Features
- Can enforce that each Turker can only do HIT once (uses http://uniqueturker.myleott.com/; see `opt['ut_id']`)
- If multiple algorithms are specified in `opt['which_algs_paths']`, then each HIT tests all algorithms randomly i.i.d. from this list.
- If `opt['paired']` is true, then "fake/n.jpg" will be pitted against "real/n.jpg"; if false, "fake/n.jpg" will be pitted against "real/m.jpg", for random n and m
- See `getDefaultOpts()` for documentation on more features

## Citation

This tool was initially developed for <a href="http://richzhang.github.io/colorization/">Colorful Image Colorization</a> in Matlab (see [this](https://github.com/phillipi/AMT_Real_vs_Fake/tree/matlab) branch). This master branch has been translated into Python. Feel free to use this <a href="http://richzhang.github.io/colorization/resources/bibtex_eccv2016_colorization.txt">bibtex</a> to cite.