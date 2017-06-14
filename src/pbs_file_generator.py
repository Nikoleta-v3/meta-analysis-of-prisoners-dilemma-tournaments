submit_script = ""
for name, min_seed, max_seed in [("0-1999", 0, 2000),
                                 ("2000-3999", 2000, 4000),
                                 ("4000-5999", 4000, 6000),
                                 ("6000-7999", 6000, 8000),
                                 ("8000-9999", 8000, 10000)]:

    pbs_file = """#!/bin/bash
#PBS -q workq
#PBS -N {}
#PBS -P PR350
#PBS -o axlml{}out.txt
#PBS -e axlml{}err.txt
#PBS -l select=1:ncpus=16:mpiprocs=16
#PBS -l place=scatter:excl
#PBS -l walltime=70:00:00

export MPLBACKEND="agg"
# Run std
cd /home/c1569433/rsc/axlml/src
/home/c1569433/anaconda3/envs/axlml/bin/python main.py /scratch/c1569433/axlml/data/ {} {} 
""".format(name, name, name, min_seed, max_seed)

    with open("pbs/{}.pbs".format(name), 'w') as f:
        f.write(pbs_file)

    submit_script += "qsub pbs/{}.pbs \n".format(name)

with open("submit_meta_workers.sh", 'w') as f:
    f.write(submit_script)

