from __future__ import division

import os

tpl_str='''#!/bin/bash
##
#@ energy_policy_tag = energy_speedup_blockswipdg_{{ MACRO }}
#@ minimize_time_to_solution = yes
# DO NOT USE environment = COPY_ALL
#@ job_type = parallel
#@ class = {{ 'test' if nodes < 17 else 'general' }}
#@ node = {{ nodes }}
#@ island_count=1,1
# other example
#@ tasks_per_node = 28
#@ wall_clock_limit = 0:05:30
##                    1 h 20 min 30 secs
#@ job_name = speedup_{{ MACRO }}_{{ nodes }}N_1C
#@ network.MPI = sn_all,not_shared,us
#@ initialdir = $(home)/build/main_gdt/gcc/dune-gdt/dune/gdt/test/
#@ output = speedup_blockswipdg_{{ MACRO }}x__{{ "%06d"|format(nodes) }}N_1C_$(jobid).out
#@ error = speedup_blockswipdg_{{ MACRO }}x__{{ "%06d"|format(nodes) }}N_1C_$(jobid).err
#@ notification=always
#@ notify_user=rene.milk@wwu.de
#@ queue
. /etc/profile
. /etc/profile.d/modules.sh
#setup of environment
source $HOME/.bashrc
#optional: 
#module load mpi_pinning/hybrid_blocked

set -eu
 
BIN=${HOME}/build/main_gdt/gcc/dune-gdt/dune/gdt/test/test_block_swipdg_discretization

RDIR="${HOME}/results/block-yaspgrid_speedup_n{{ "%06d"|format(procs) }}_{{ MACRO }}x__T1"
[[ -d ${RDIR} ]] || mkdir -p ${RDIR}

OPT="{{ cwd }}/block_speedup.ini -global.datadir ${RDIR} "
OPT="{{ cwd }}/block_speedup.ini -global.datadir ${RDIR} -grid.num_elements {{ MACRO }} "

poe $BIN ${OPT}
'''

from jinja2 import Template
tpl=Template(tpl_str)

def output_run(i,doublings):
    nodes = int(pow(2,i))
    MACRO=386*doublings
    procs = 28 * nodes
    cwd = os.getcwd()
    #print('nodes {} - procs {}'.format(nodes, procs))
    fn = 'speedup_node_{}.submit'.format(nodes)
    open(fn, 'wt').write(tpl.render(**locals()))
    print('llsubmit {}'.format(fn))

start = 5
doublings = 6
for i in range(start,start+doublings+1):
    output_run(i,start+doublings)

