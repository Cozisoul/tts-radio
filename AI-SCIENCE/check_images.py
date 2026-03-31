#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND-revision/intropyproject-classify-pet-images/check_images.py
#
# TODO 0: Add your information below for Programmer & Date Created.                                                     
# PROGRAMMER: Thapelo Madiba Masebe
# DATE CREATED: 09/10/2025
# REVISED DATE:
# PURPOSE: Classifies pet images using a pretrained CNN model, compares these
#          classifications to the true identity of the pets in the images, and
#          summarizes how well the CNN performed on the image classification task.
#          Note that the true identity of the pet (or object) in the image is
#          indicated by the filename of the image. Therefore, your program must
#          first extract the pet image label from the filename before
#          classifying the images using the pretrained CNN model. With this
#          program we will be comparing the performance of 3 different CNN model
#          architectures to determine which provides the 'best' classification.
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# -------------------------- Imports --------------------------------
from time import time, sleep

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Imports functions created for this program
from get_input_args import get_input_args
from get_pet_labels import get_pet_labels
from classify_images import classify_images
from adjust_results4_isadog import adjust_results4_isadog
from calculates_results_stats import calculates_results_stats
from print_results import print_results

# -------------------------- Main ------------------------------------
def main():
    # TODO 0: Measures total program runtime by collecting start time
    start_time = time()

    # TODO 1: Retrieve command‑line arguments
    # This function returns a Namespace with attributes:
    #   .dir   – directory containing images
    #   .arch  – architecture to use
    #   .dogfile – file that contains dog names
    in_arg = get_input_args()

    # Function that checks command line arguments using in_arg  
    check_command_line_arguments(in_arg)

    # TODO 2: Create pet image labels from filenames
    results = get_pet_labels(in_arg.dir)

    # Function that checks Pet Images in the results Dictionary using results    
    check_creating_pet_image_labels(results)

    # TODO 3: Classify images and compare to ground truth
    classify_images(in_arg.dir, results, in_arg.arch)

    # Function that checks Results Dictionary using results    
    check_classifying_images(results)    

    # TODO 4: Adjust results dictionary to mark "is a dog" flags
    adjust_results4_isadog(results, in_arg.dogfile)

    # Function that checks Results Dictionary for is-a-dog adjustment using results
    check_classifying_labels_as_dogs(results)

    # TODO 5: Calculate result statistics
    results_stats = calculates_results_stats(results)

    # Function that checks Results Statistics Dictionary using results_stats
    check_calculating_results(results, results_stats)

    # TODO 6: Print final results
    print_results(results, results_stats, in_arg.arch, True, True)

    # TODO 0: Measure total program runtime by collecting end time
    end_time = time()

    # TODO 0: Compute overall runtime in seconds & print it in hh:mm:ss format
    tot_time = end_time - start_time
    hh = int(tot_time // 3600)
    mm = int((tot_time % 3600) // 60)
    ss = int(tot_time % 60)
    print("\n** Total Elapsed Runtime: {:02d}:{:02d}:{:02d}".format(hh, mm, ss))

# Call to main function to run the program
if __name__ == "__main__":
    main()
