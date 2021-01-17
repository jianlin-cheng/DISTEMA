"""
@ Description: Generate difference map
@ Author: Shawn Chen
@ Created Date: 2021-01-17
@ last updated: 2021-01-17
"""

import os
import numpy as np
import argparse
import multiprocessing as mp


# add arugument
parser = argparse.ArgumentParser(
    usage='python generate_difference_map.py ...',
    description='Generate difference map'
    )

parser.add_argument('-c', '--cores', default='1', help='multi-cores number', required=False)
parser.add_argument('-s', '--server_model', help='server model distance maps path', required=True)
parser.add_argument('-p', '--perdicted_map', help='DeepDist predicted distance map', required=True)
parser.add_argument('-o', '--output_folder', help='Output folder', required=True)
args = parser.parse_args()

# load parameters
multi_core = int(args.cores)
server_model_path = os.path.abspath(args.server_model)
predicted_map = os.path.abspath(args.perdicted_map)
output_folder = os.path.abspath(args.output_folder)

os.makedirs(output_folder, exist_ok=True)


def helper(seq_dist, pdb_dist, output_):
    """
    Generatd distance map by filter and keep upper triangle
    Args:
        seq_dist: DeepDist predicted distance map
        pdb_dist: server model distance 
        output_: output path

    Returns:
        None
    """
    # read two distance map
    seq_file = np.loadtxt(seq_dist)
    np.fill_diagonal(seq_file, 0) 
    pdb_file = np.loadtxt(pdb_dist, skiprows=1)  # remove header

    # only keep the element which value is smaller or equal than 16
    dim = seq_file.shape[0]
    filtered_seq_file = np.zeros_like(seq_file)
    filtered_pdb_file = np.zeros_like(pdb_file)

    for idx_row in range(dim):
        for idx_col in range(idx_row, dim):
            if seq_file[idx_row, idx_col] <= 16 and pdb_file[idx_row, idx_col] <= 16:
                filtered_seq_file[idx_row, idx_col] = seq_file[idx_row, idx_col]
                filtered_pdb_file[idx_row, idx_col] = pdb_file[idx_row, idx_col]

    diff = np.abs(np.subtract(filtered_seq_file, filtered_pdb_file))
    np.savetxt(fname=output_, X=diff)
    return None


if __name__ == '__main__':
    parameter_list = []
    
    for item in os.listdir(server_model_path):
        pdb_map = os.path.join(server_model_path, item)
        model_name = item.split('.')[0]
        output_file = os.path.join(output_folder, model_name + '.txt')
        parameter_list.append([predicted_map, pdb_map, output_file])
        
    p = mp.Pool(multi_core)
    for parameter in parameter_list:
        p.apply_async(helper, parameter)
    p.close()
    p.join()

    print('Generated distance map.')