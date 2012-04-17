#!/usr/bin/env python

# Script: stress2press.py
# Author: Mario Orsi (orsimario at gmail.com, www.soton.ac.uk/~orsi)
# Purpose: Reads a file containing stress components (calculated
#          with the LAMMPS commands 'compute stress/atom' and
#          'fix ave/spatial'), and converts to corresponding pressures
# Syntax: stress2press.py inputFile area Pn
# Example: stress2press.py stress.zProfile 4650 1.0 > lpp.dat
# Notes: - inputFile = LAMMPS output file generated by fix ave/spatial
#        - area = xy surface area of slabs [Angstrom^2]
#        - Pn = normal pressure [atm]
# References: - http://lammps.sandia.gov/doc/compute_stress_atom.html
#             - Thompson et al, J Chem Phys 131, 154107 (2009)
#             - Orsi & Essex, PLoS ONE 6, e28637 (2011), p. 11
#             - Orsi et al, J Phys Condens Matter 22, 155106 (2010),
#               section 5.2

import sys, string

if len(sys.argv) != 4:
  print "Syntax: stress2press.py inputFile area Pn"
  sys.exit()

inFileName = sys.argv[1]
area = float(sys.argv[2])
Pn = float(sys.argv[3])
inFile = open(inFileName, "r")
lines = inFile.readlines()
inFile.close()

# find slab thickness (delta):
for line in lines:
    if line[0] != '#': # ignore comments
        words = string.split(line)
        if len(words) == 2:
            nBins = int(words[1])
        else:
            if int(words[0]) == 1:
                coordLower = float(words[1])
            if int(words[0]) == nBins:
                coordUpper = float(words[1])
delta = abs( coordUpper - coordLower ) / ( nBins - 1 )
slabVolume = area * delta

# calc & output P tensor components (file) and P_L-P_N (screen):
outFile = open('zP_xx_yy_zz_xy_xz_yz.dat', 'w')
for line in lines:
    if line[0] != '#': # ignore comments
        words = string.split(line)
        if len(words) != 2:
            coord = float(words[1])
            nCount = float(words[2])
            xxStress = float(words[3]) * nCount / slabVolume
            yyStress = float(words[4]) * nCount / slabVolume
            zzStress = float(words[5]) * nCount / slabVolume  
            xyStress = float(words[6]) * nCount / slabVolume
            xzStress = float(words[7]) * nCount / slabVolume  
            yzStress = float(words[8]) * nCount / slabVolume  
            Pxx = -xxStress
            Pyy = -yyStress
            Pzz = -zzStress
            Pxy = -xyStress
            Pxz = -xzStress
            Pyz = -yzStress          
            outFile.write( '%f %f %f %f %f %f %f\n' %
                           (coord,Pxx,Pyy,Pzz,Pxy,Pxz,Pyz) )
            latPressProf = 0.5 * ( Pxx + Pyy ) - Pn
            print coord, latPressProf # [A, atm]
outFile.close()
