#!/usr/bin/env python

#   perf-libs-tools
#   Copyright 2017 Arm Limited. 
#   All rights reserved.

import matplotlib.pyplot as plt
import numpy as np
import pylab
import math

import argparse		# Commandline argument parsing
import os		# File directory structure parsing
import json		# Needed for JSON input/output
import time		# Used for getting the current date/time

import matplotlib

from matplotlib.patches import Shadow

def parse_options():

# Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", dest='inFile', default='')
    parser.add_argument("-l", "--legend", help="Show graph legend", dest='showLegend', default=False, action='store_true')
#    parser.add_argument("-n", "--normalize", help="Normalize bars to percentages of max", dest='normalizeBars', default=False, action='store_true')
#    parser.add_argument("-x", "--exclude", help="Exclude unrepresented functions", dest='excludeZeroes', default=False, action='store_true')

    # Parse arguments
    args = parser.parse_args()
    return args


def main(args=None):
    print 'DGEMM heatmap creation'
    args = parse_options()

    generate_heatmap(args)

def generate_heatmap(args):
    

    if (args.inFile) :
        a = np.loadtxt(args.inFile)
    else :
        print 'Showing example data.  Use "-i" option to select your own input.'
        a = np.loadtxt('tools/EXAMPLES/armpl-example.dgemm')

    maxvala = a.max()
#    print maxvala
    
    b = np.zeros_like(a)
    for i in range (0, 5):
        for j in range (0, 5):
            b[i][j] = a[i+12][j]
            b[i+5][j] = a[i+17][j]
    
    maxvalb = b.max()
#    print maxvalb
#    a = a
    for i in range (0, 5):
        for j in range (0, 5):
            b[i][j] = b[i][j]/maxvalb*maxvala
#    print b
   
#    plt.ion()

#    plt.title("DGEMM for HPL")
#    plt.show()
    fig = plt.figure()
    fig.canvas.set_window_title('DGEMM heatmaps - %s' % args.inFile) 
    plt.subplot(231)
    plt.xlabel('K (10^x))')
    plt.ylabel('M (10^y))')
    plt.title("A-shape - count")
    plt.imshow(a[0:5], cmap='gist_heat', interpolation='nearest', origin='lower', extent=(0.0,5.0,0.0,5.0), aspect='equal')
#    plt.colorbar()

    plt.subplot(232)
    plt.xlabel('N (10^x))')
    plt.ylabel('K (10^y))')
    plt.title("B-shape - count")
    plt.imshow(a[5:10], cmap='gist_heat', interpolation='nearest', origin='lower', extent=(0.0,5.0,0.0,5.0), aspect='equal')

    plt.subplot(234)
    plt.xlabel('K (10^x))')
    plt.ylabel('M (10^y))')
    plt.title("A-shape - time")
    plt.imshow(b[0:5], cmap='gist_heat', interpolation='nearest', origin='lower', extent=(0.0,5.0,0.0,5.0), aspect='equal')
#    plt.colorbar()

    plt.subplot(235)
    plt.xlabel('N (10^x))')
    plt.ylabel('K (10^y))')
    plt.title("B-shape - time")
    plt.imshow(b[5:10], cmap='gist_heat', interpolation='nearest', origin='lower', extent=(0.0,5.0,0.0,5.0), aspect='equal')
    

    pt_tot = np.sum(a[0:5])
    nn_tot = a[10][0]/pt_tot*100.0
    nt_tot = a[10][1]/pt_tot*100.0
    tn_tot = a[10][2]/pt_tot*100.0
    tt_tot = a[10][3]/pt_tot*100.0

#    print b[0:5]
    pt_t_tot = np.sum(b[0:5])
#    print pt_t_tot
    nn_t_tot = a[11][0]/maxvalb*maxvala/pt_t_tot*100.0
    nt_t_tot = a[11][1]/maxvalb*maxvala/pt_t_tot*100.0
    tn_t_tot = a[11][2]/maxvalb*maxvala/pt_t_tot*100.0
    tt_t_tot = a[11][3]/maxvalb*maxvala/pt_t_tot*100.0

#    print pt_t_tot, nn_t_tot, nt_t_tot, tn_t_tot, tt_t_tot

# make a square figure and axes
    labels = ['NN', 'NT', 'TN', 'TT']
    sizes = [nn_tot, nt_tot, tn_tot, tt_tot]
    sizes_t = [nn_t_tot, nt_t_tot, tn_t_tot, tt_t_tot]

    if (tt_tot == 0) :
        labels.pop(3)
        sizes.pop(3)
        sizes_t.pop(3)
    if (tn_tot == 0) :
        labels.pop(2)
        sizes.pop(2)
        sizes_t.pop(2)
    if (nt_tot == 0) :
        labels.pop(1)
        sizes.pop(1)
        sizes_t.pop(1)
    if (nn_tot == 0) :
        labels.pop(0)
        sizes.pop(0)
        sizes_t.pop(0)

    expl_arr = np.zeros_like(sizes)
    expl_arr = expl_arr + 0.05

    plt.subplot(233)
    plt.pie(sizes, explode=expl_arr, labels=labels, autopct='%1.0f%%', shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.subplot(236)
    plt.pie(sizes_t, explode=expl_arr, labels=labels, autopct='%1.0f%%', shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    print 'Done!'
    
    
    plt.show(block=True)
    plt.figure(num='This is the title')


# Footer for catching no main
if __name__ == '__main__':
    main()
    