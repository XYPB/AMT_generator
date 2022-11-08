import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from scipy import stats
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--res_dir', type=str)
parser.add_argument('--N_practice', type=int, default=5)
parser.add_argument('--N_imgs', type=int, default=21)
parser.add_argument('--remove_fail', action='store_true')
parser.add_argument('--gt', type=str, default='CondAVTransformer_VNet_randshift_2s_GH_vqgan')
parser.add_argument('--match_list_path', type=str, default='../SpecVQGAN/data/AMT_test/match_list.json')
parser.add_argument('--action_match', action='store_true')
parser.add_argument('--action_mismatch', action='store_true')
parser.add_argument('--addition_exp_res', default=None)
parser.add_argument('--new_html', action='store_true')

def mean_pm(p, n):
    import scipy.stats
    if not (n*p > 5 and n*(1-p) > 5):
        print('Not enough samples for normal approximation (doing anyway)')
    alpha = 0.05
    z = scipy.stats.norm.ppf(1-0.5*alpha)
    edge = z*np.sqrt(1./n*p*(1-p))
    return edge

def mean_pm_normal(stdev, n):
    import scipy.stats
    alpha = 0.05
    z = scipy.stats.norm.ppf(1-0.5*alpha)
    edge = z*np.sqrt(1./n)*stdev
    return edge

def ci(stderr):
    return 1.96 * stderr

def ci_str(mean_val, stderr):
    return '%.2f%% \\pm %.2f' % (100*mean_val, 100*ci(stderr))

def mean_pm_str(p, n):
    return '%.2f%% \\pm %.2f' % (100*p, 100*mean_pm(p, n))

def gather_csv(args):
    df = None
    for filename in os.listdir(args.res_dir):
        if filename == 'approved.csv':
            continue
        filename = os.path.join(args.res_dir, filename)
        if '.csv' not in filename: continue
        if df is None:
            df = pd.read_csv(filename, header=0)
        else:
            df = pd.concat([df, pd.read_csv(filename, header=0)], axis=0, ignore_index=True)
    return df


def stderr(ratio, n):
    x = np.zeros(n)
    hit_cnt = int(n * ratio)
    x[:hit_cnt] = 1
    return stats.sem(x)


def plot_res(ratio, arr, pval, exp):
    plt.figure()
    x = range(len(ratio))
    k = sorted(list(ratio.keys()))
    y = [ratio[kk] for kk in k]
    a = [arr[kk] for kk in k]
    ps = [pval[kk] for kk in k]
    plt.bar(x, y, label=exp, alpha=0.8)
    plt.hlines(0.5, -0.5, len(x) - 0.5, color='orange', alpha=0.5)
    for i in range(len(x)):
        mean_val = np.mean(a[i])
        n = len(a[i])
        conf_inter = mean_pm_str(mean_val, n)
        std = stderr(mean_val, n)
        print(n)
        print(conf_inter)
        print(std)
        # print(ci_str(y[i], std))
        plt.text(x[i], y[i], conf_inter, ha='center', va='bottom', fontsize=9)
        plt.text(x[i], y[i]+0.05, f'{ps[i]:.3f}', ha='center', va='bottom', color='blue')
    plt.xticks(x, k, rotation=60)
    plt.ylim(0, 1)
    plt.legend()
    plt.savefig(os.path.join(args.res_dir, f'res_{exp}.png'), dpi=300, bbox_inches='tight', pad_inches=0.2)


def gt_equal(s, gt):
    return s != gt and s.replace('_no_earlystop', '') != gt


if __name__ == "__main__":
    args = parser.parse_args()
    df = gather_csv(args)
    match_list = json.load(open(args.match_list_path, 'r'))
    algo_pre_str = 'Answer' if args.new_html else 'Input'

    ans_timbre = {}
    ans_sync = {}
    col_names = df.columns.values.tolist()
    cnt = 0
    for i in range(df.shape[0]):
        flg = False
        for j in range(args.N_practice, args.N_imgs):
            if df.at[i, f'Answer.selection_sync{j}'] == 'vigilance' or df.at[i, f'Answer.selection_timbre{j}'] == 'vigilance':
                flg = True
                df.loc[i, 'Reject'] = 'We are so sorry that we cannot approve your submission since it has failed on the sentinel examples we provided during the test.'
                df.loc[i, 'Approve'] = ''
                break
        if flg and args.remove_fail:
            continue
        elif args.remove_fail:
            df.loc[i, 'Approve'] = 'x'
            df.loc[i, 'Reject'] = ''
        cnt += 1
        for j in range(args.N_practice, args.N_imgs):
            if gt_equal(df.at[i, f'{algo_pre_str}.algo_A{j}'], args.gt):
                pair = 'vs_' + df.at[i, f'{algo_pre_str}.algo_A{j}']
            else:
                pair = 'vs_' + df.at[i, f'{algo_pre_str}.algo_B{j}']
            if 'vigilance' in pair:
                continue
            # task_idx = int(df.at[i, f'{algo_pre_str}.image_A{j}'].split('/')[-1].split('.')[0])

            # if args.action_match and not match_list[task_idx]:
            #     continue
            # if args.action_mismatch and match_list[task_idx]:
            #     continue

            pair = pair.replace('CondAVTransformer_VNet_randshift_2s_', '').replace('_GH_vqgan', '').replace('_no_earlystop', '')
            if pair not in ans_timbre.keys():
                ans_timbre[pair] = []
            ans_timbre[pair].append(df.at[i, f'Answer.selection_timbre{j}'])
            if pair not in ans_sync.keys():
                ans_sync[pair] = []
            ans_sync[pair].append(df.at[i, f'Answer.selection_sync{j}'])
    print(cnt, '\n')
    json.dump(ans_timbre, open(os.path.join(args.res_dir, 'ans_timbre.json'), 'w'))
    json.dump(ans_sync, open(os.path.join(args.res_dir, 'ans_sync.json'), 'w'))

    if args.addition_exp_res is not None:
        for additional_exp in args.addition_exp_res.strip().split(','):
            add_ans_timbre = json.load(open(os.path.join(additional_exp, 'ans_timbre.json'), 'r'))
            add_ans_sync = json.load(open(os.path.join(additional_exp, 'ans_sync.json'), 'r'))
            for k in ans_timbre.keys():
                ans_timbre[k] += add_ans_timbre[k]
                ans_sync[k] += add_ans_sync[k]

    timbre_ratio = {}
    timbre_arr = {}
    timbre_pval = {}
    sync_ratio = {}
    sync_arr = {}
    sync_pval = {}
    for p in ans_timbre.keys():
        timbre_ratio[p] = len([t for t in ans_timbre[p] if gt_equal(t, args.gt)]) / len(ans_timbre[p])
        timbre_arr[p] = [1 if gt_equal(t, args.gt) else 0 for t in ans_timbre[p]]
        timbre_pval[p] = stats.binom_test(len([t for t in ans_timbre[p] if gt_equal(t, args.gt)]), len(ans_timbre[p]), 0.5, alternative='greater')
        sync_ratio[p] = len([t for t in ans_sync[p] if gt_equal(t, args.gt)]) / len(ans_sync[p])
        sync_arr[p] = [1 if gt_equal(t, args.gt) else 0 for t in ans_sync[p]]
        sync_pval[p] = stats.binom_test(len([t for t in ans_sync[p] if gt_equal(t, args.gt)]), len(ans_sync[p]), 0.5, alternative='greater')
    print('timbre', timbre_ratio, '\n')
    print('sync', sync_ratio)

    print('timbre', timbre_pval, '\n')
    print('sync', sync_pval)

    timbre_exp = 'timbre'
    sync_exp = 'sync'
    if args.action_match:
        timbre_exp += '_match'
        sync_exp += '_match'
    if args.action_mismatch:
        timbre_exp += '_mismatch'
        sync_exp += '_mismatch'
    plot_res(timbre_ratio, timbre_arr, timbre_pval, timbre_exp)

    plot_res(sync_ratio, sync_arr, sync_pval, sync_exp)

    if args.remove_fail:
        df.to_csv(os.path.join(args.res_dir, 'approved.csv'))




