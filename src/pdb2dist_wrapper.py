"""
@ Description: wrapper for pdb2dist
@ Author: Shawn Chen
@ Create Date: 2021-01-17
@ Last Update: 2021-01-17
"""

import os
import sys
import subprocess
import argparse
import glob


parser = argparse.ArgumentParser(
    usage = 'python pdb2dist_wrapper.py',
    description = 'wrapper for pdb2dist'
)

parser.add_argument('-i', '--input', help='Input server model folder', required=True)
parser.add_argument('-f', '--fasta', help='sequence fasta file', required=True)
parser.add_argument('-o', '--output', help='Output folder', required=True)
args = parser.parse_args()

input_folder = args.input
fasta_file = args.fasta
output_folder = args.output

if not os.path.isdir(input_folder):
    print('The input folder does not exist.')
    print('Please check {}'.format(input_folder))
    sys.exit(1)

os.makedirs(output_folder, exist_ok=True)
script_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    for item in os.listdir(input_folder):
        pdb_file = os.path.join(input_folder, item)
        cmd = f'python {script_path}/pdb2dist.py {pdb_file} {fasta_file} {output_folder}'
        subprocess.call(cmd, shell=True)
    
    for item in glob.glob(os.path.join(output_folder, '*.dist')):
        os.remove(item)

    print('Done')   