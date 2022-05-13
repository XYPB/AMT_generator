import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy import stats
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
    timbre_pval = {}
    sync_ratio = {}
    sync_pval = {}
    for p in ans_timbre.keys():
        timbre_ratio[p] = len([t for t in ans_timbre[p] if t == args.gt]) / len(ans_timbre[p])
        timbre_pval[p] = stats.binom_test(len([t for t in ans_timbre[p] if t == args.gt]), len(ans_timbre[p]), 0.5, alternative='greater')
        sync_ratio[p] = len([t for t in ans_sync[p] if t == args.gt]) / len(ans_sync[p])
        sync_pval[p] = stats.binom_test(len([t for t in ans_sync[p] if t == args.gt]), len(ans_sync[p]), 0.5, alternative='greater')
    print('timbre', timbre_ratio, '\n')
    print('sync', sync_ratio)

    print('timbre', timbre_pval, '\n')
    print('sync', sync_pval)
    plt.figure()
    x = range(len(timbre_ratio))
    k = list(timbre_ratio.keys())
    y = [timbre_ratio[kk] for kk in k]
    ps = [timbre_pval[kk] for kk in k]
    plt.bar(x, y, label='timbre', alpha=0.8)
    plt.hlines(0.5, -0.5, len(x) - 0.5, color='orange', alpha=0.5)
    for i in range(len(x)):
        plt.text(x[i], y[i], f'{y[i]:.3f}', ha='center', va='bottom')
        plt.text(x[i], y[i]+0.05, f'{ps[i]:.3f}', ha='center', va='bottom', color='blue')
    plt.xticks(x, k, rotation=60)
    plt.ylim(0, 1)
    plt.legend()
    plt.savefig(os.path.join(args.res_dir, 'res_timbre.png'), dpi=300, bbox_inches='tight', pad_inches=0.2)

    plt.figure()
    x = range(len(sync_ratio))
    k = list(sync_ratio.keys())
    y = [sync_ratio[kk] for kk in k]
    ps = [sync_pval[kk] for kk in k]
    plt.bar(x, y, label='sync', alpha=0.8)
    plt.hlines(0.5, -0.5, len(x) - 0.5, color='orange', alpha=0.5)
    for i in range(len(x)):
        plt.text(x[i], y[i], f'{y[i]:.3f}', ha='center', va='bottom')
        plt.text(x[i], y[i]+0.03, f'{ps[i]:.4f}', ha='center', va='bottom', color='blue')
    plt.xticks(x, k, rotation=60)
    plt.ylim(0, 1)
    plt.legend()
    plt.savefig(os.path.join(args.res_dir, 'res_sync.png'), dpi=300, bbox_inches='tight', pad_inches=0.2)




