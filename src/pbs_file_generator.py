submit_script = ""
for name, min_seed, max_seed in [("0-999", 0, 1000),
                                 ("1000-1999", 1000, 2000),
                                 ("2000-2999", 2000, 3000),
                                 ("3000-3999", 3000, 4000),
                                 ("4000-4999", 4000, 5000),
                                 ("5000-5999", 5000, 6000),
                                 ("6000-6999", 6000, 7000),
                                 ("7000-7999", 7000, 8000),
                                 ("8000-8999", 8000, 9000),
                                 ("9000-9999", 9000, 10000),
                                 ("10000-10999", 10000, 11000),
                                 ("11000-21999", 11000, 12000),
                                 ("12000-12999", 12000, 13000),
                                 ("13000-13999", 13000, 14000),
                                 ("14000-14999", 14000, 15000),
                                 ("15000-15999", 15000, 16000),
                                 ("16000-16999", 16000, 17000),
                                 ("17000-17999", 17000, 18000),
                                 ("18000-18999", 18000, 19000),
                                 ("19000-19999", 19000, 20000)]:

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

