#!/bin/bash

root -l -q 'plotConfRegions1D.C("/home/sam/EFTfitterRelease/examples/EFTfitter-combined-model/veryhigh_results_a_w_8_cpq-cptb-cptbI-cbw-ctw-cqq-P-phases_/result_plots.root")'


root -l -q 'plotConfRegions2D.C("/home/sam/EFTfitterRelease/examples/EFTfitter-combined-model/veryhigh_results_a_w_8_cpq-cptb-cptbI-cbw-ctw-cqq-P-phases_/result_plots.root")'


root -l -q 'combineConfRegions2D.C("/home/sam/EFTfitterRelease/examples/EFTfitter-combined-model/veryhigh_results_a_w_8f_cpq-cptb-cbw-ctw-cqq-P_/result_plots.root","/home/sam/EFTfitterRelease/examples/EFTfitter-combined-model/veryhigh_results_a_w_8_cpq-cptb-cbw-ctw-cqq-P_/result_plots.root")'




