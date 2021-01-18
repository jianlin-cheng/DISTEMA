"""
@ Description: Eestimation of Protein Model Accuracy
@ Author: Shawn Chen
@ Create Date: 2021-01-17
@ Laste Date: 2021-01-17
"""


import os
import torch
from model import mynet
import argparse
from util import predict_single
import pandas as pd
import numpy as np
import sys

parser = argparse.ArgumentParser(
    usage = 'python eval_gpu.py difference_map_folder/',
    description = 'Eetimation of protein model accuacy.'
)

parser.add_argument('-i', '--input', help='Input Difference map folder', required=True)
parser.add_argument('-o', '--output', help='Output folder', required=True)
parser.add_argument('-m', '--model', help='pretrain model', required=True)
parser.add_argument('-g', '--gpu', help='GPU device', default='cuda', required=False)
args = parser.parse_args()

input_folder = os.path.abspath(args.input)
output_folder = os.path.abspath(args.output)
pretrain_model = os.path.abspath(args.model)

device = torch.device(args.gpu)


if not os.path.isdir(input_folder):
    print('The input folder does not exist.')
    print('Please check {}'.format(input_folder))
    sys.exit(1)

os.makedirs(output_folder, exist_ok=True)


if __name__ == '__main__':
    model_name_list = []
    yhat_list = []
    
    # initial model
    net = mynet()
    
    # load pretrained model
    if args.gpu == 'cuda':
        net.load_state_dict(torch.load(pretrain_model))
    else:
        net.load_state_dict(torch.load(pretrain_model, map_location='cpu'))
    model = net.to(device)
    
    # turn on eval mode
    model.eval()
    
    # read data
    for item in os.listdir(input_folder):
        model_name = item.split('.')[0]
        model_name_list.append(model_name)
        x_data = torch.from_numpy(np.loadtxt(os.path.join(input_folder, item)))
        x_data = x_data.to(device, dtype=torch.float)
        x_shape = x_data.shape
        x_data = x_data.view(1,1, x_shape[0], x_shape[1])
        y_hat = predict_single_gpu(model, x_data)
        yhat_list.append(y_hat.item())
    
    res = pd.DataFrame(list(zip(model_name_list, yhat_list)), columns=['model', 'pred_gdtts'])
    res.sort_values(by='pred_gdtts', ascending=['pred_gdtts'], inplace=True)
    res.to_csv(os.path.join(output_folder, 'ans.csv'), index=False)
    print('Evaluated')

    

        