import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--res_dir', type=str)
parser.add_argument('--N_practice', type=int, default=5)
parser.add_argument('--N_imgs', type=int, default=20)
parser.add_argument('--gt', type=str, default='CondAVTransformer_VNet_randshift_2s_GH_vqgan')

def gather_cav(args):
    df = None
    for filename in os.listdir(args.res_dir):
        filename = os.path.join(args.res_dir, filename)
        if '.csv' not in filename: continue
        if df is None:
            df = pd.read_csv(filename, header=0)
        else:
            df = pd.concat([df, pd.read_csv(filename, header=0)], axis=0, ignore_index=True)
    return df


if __name__ == "__main__":
    args = parser.parse_args()
    df = gather_cav(args)

    ans_timbre = {}
    ans_sync = {}
    col_names = df.columns.values.tolist()
    for i in range(df.shape[0]):
        for j in range(args.N_practice, args.N_imgs):
            if df.at[i, f'Input.algo_A{j}'] != args.gt:
                pair = 'vs_' + df.at[i, f'Input.algo_A{j}']
            else:
                pair = 'vs_' + df.at[i, f'Input.algo_B{j}']
            pair = pair.replace('CondAVTransformer_VNet_randshift_2s_', '').replace('_GH_vqgan', '')
            if pair not in ans_timbre.keys():
                ans_timbre[pair] = []
            ans_timbre[pair].append(df.at[i, f'Answer.selection_timbre{j}'])
            if pair not in ans_sync.keys():
                ans_sync[pair] = []
            ans_sync[pair].append(df.at[i, f'Answer.selection_sync{j}'])

    timbre_ratio = {}
    sync_ratio = {}
    for p in ans_timbre.keys():
        timbre_ratio[p] = len([t for t in ans_timbre[p] if t == args.gt]) / len(ans_timbre[p])
        sync_ratio[p] = len([t for t in ans_sync[p] if t == args.gt]) / len(ans_sync[p])
    print('timbre', timbre_ratio, '\n')
    print('sync', sync_ratio)
    plt.figure()
    plt.bar(range(len(timbre_ratio)), list(timbre_ratio.values()), label='timbre', alpha=0.5)
    plt.bar(range(len(sync_ratio)), list(sync_ratio.values()), label='sync', alpha=0.5)
    plt.xticks(range(len(timbre_ratio)), list(timbre_ratio.keys()), rotation=45)
    plt.legend()
    plt.savefig(os.path.join(args.res_dir, 'res.png'), dpi=300, bbox_inches='tight', pad_inches=0.2)




