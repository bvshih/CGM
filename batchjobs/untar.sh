#!/bin/bash
#----------------------------------------------------
# Extract 
#----------------------------------------------------
#SBATCH -J  untar           # Job name
#SBATCH -o /scratch/08263/tg875625/CGM/batchjobs/script_outs/untar_%j.o       # Name of stdout output file
#SBATCH -e /scratch/08263/tg875625/CGM/batchjobs/script_outs/untar_%j.e       # Name of stderr error file
#SBATCH -p normal          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes (must be 1 for serial)
#SBATCH -n 1               # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t 10:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=bv.shih@gmail.com
#SBATCH --mail-type=all    # Send email at begin and end of job

# Other commands must follow all #SBATCH directives...

date

cd /scratch/08263/tg875625/CGM/GMs/

pwd

tar -xvf /scratch/06040/adcruz/GMs/pioneer50h243.1536gst1bwK1BH.tar
