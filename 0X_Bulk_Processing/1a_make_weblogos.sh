#!/bin/bash

# Make weblogos for every MEME file in `02_Call_RefPT/PWM/*.meme.txt`

### CHANGE ME
WRK=/path/to/2024-Chen_Nature/0X_Bulk_Processing
WRK=/storage/home/owl5022/scratch/2024-Chen_Nature/0X_Bulk_Processing
###

# Dependencies
# - ceqlogo

set -exo
module load anaconda
conda activate bx

# Fill in placeholder constants with your directories
PWM=$WRK/../02_Call_RefPT/PWM
OUTDIR=$WRK/Library/WebLogos

# Set up output directories
[ -d $OUTDIR ] || mkdir -p $OUTDIR

# Loop through the PWM files
for PWMFILE in $PWM/*.meme.txt;
do
    BASE=`basename $PWMFILE ".meme.txt"`
    # Generate logo
    ceqlogo -i $PWMFILE -m 1 -o $OUTDIR/$BASE\_logo.eps -f EPS
done
