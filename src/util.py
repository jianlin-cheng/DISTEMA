"""
@ Description: helper functions
@ Author: Shawn Chen
@ Create date: 2020-12-29
@ Last Update: 2020-01-18
"""

import pandas as pd
import torch
import numpy as np


def predict_single(md, single_data):
    """
        turn on eval mode, and load model to GPU before call this funtion
    """
    with torch.no_grad():
        y_hat_single = md(single_data)  # gpu
    return y_hat_single

# def predict_single_cpu(md, single_data):
#     # TODO
#     """
#         turn on eval mode, and load model to cpu beforem call this function
#     """
#     with torch.no_grad():
#         y_hat_single = md(single_data)
#     return y_hat_single
#     return None

def ranking_loss(df):
    df.loc[:, 'target'] = df.loc[:, 'index_col'].apply(lambda x: x.split(':')[0])
    df.drop('index_col', axis=1, inplace=True)
    target_list = df['target'].unique().tolist()
    collection = []
    for i in target_list:
        tmp = df[df['target'] == i]
        max_lga = tmp['y'].max()
        max_yhat_lg = tmp.loc[tmp['y_hat'].idxmax(), 'y']
        collection.append(np.abs(float(max_lga) - float(max_yhat_lg)))
    return np.mean(collection)