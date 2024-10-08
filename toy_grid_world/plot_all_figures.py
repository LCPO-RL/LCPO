import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import pandas as pd
import os

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    'legend.fontsize': 6,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'axes.labelsize': 8,
    'axes.titlesize': 8,
    'figure.labelsize': 8,
    'figure.titlesize': 8,
    'hatch.linewidth': 0.5
})


########################################################################################################################
# ############################################### Load and plot results ################################################
########################################################################################################################

os.makedirs('./figures/', exist_ok=True)

list_files = [
    [f'./tests/a2c_grid_seed{sd}/' for sd in [19, 15, 16, 8]],
    [f'./tests/a2c_tab_grid_seed{sd}/' for sd in [5, 8, 11, 21]],
    [f'./tests/lcpo_grid_seed{sd}/' for sd in [0, 2, 3, 4]]
]
list_labels = ['a2c', 'a2c_tab', 'lcpo']

assert len(list_labels) == len(list_files)

df_list = [[] for i in range(len(list_files))]
for ind in trange(len(list_files)):
    for path in list_files[ind]:
        variant = pd.read_pickle(f'{path}/tb.pkl')
        extracted = variant['State/episode_reward']
        extracted = extracted[~np.isnan(extracted)]
        assert len(extracted) > 0
        extracted2 = variant['Grid/Up_0']
        extracted2 = extracted2[~np.isnan(extracted2)]
        assert len(extracted2) > 0
        extracted3 = variant['Grid/Left_1']
        extracted3 = extracted3[~np.isnan(extracted3)]
        assert len(extracted3) > 0
        df_dict = {'reward': extracted, 'pi_0': extracted2, 'pi_1': extracted3, 'time': np.arange(len(extracted)),
                   'seed': len(df_list[ind])}
        df_list[ind].append(pd.DataFrame(df_dict))
for i in range(len(df_list)):
    df_list[i] = pd.concat(df_list[i], ignore_index=True)

fig, ax = plt.subplots(1, 1, figsize=(3.25, 1.5))
bases = ['A2C', 'Tabular A2C', 'LCPO']

for dfi, label, color, lst in zip([0, 1, 2], bases, ['C3', 'C9', 'C2'], ['--', ':', '-']):
    df = df_list[dfi]
    st = df['time'].max() // 1000
    df['tint'] = (df['time'] / st).astype(int)
    rew = df.groupby('tint').mean()['reward']
    rew_up = df.groupby('tint').max()['reward']
    rew_dn = df.groupby('tint').min()['reward']
    tint = df.groupby('tint').mean().reset_index()['tint'] * st / 1000

    ax.plot(tint, rew, label=label, color=color, linestyle=lst)
    ax.fill_between(tint, rew_up, rew_dn, color=color, alpha=0.1, linestyle=lst)

ax.grid()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False)

ax.legend(loc='center')
plt.ylim(top=-3, bottom=-20)
plt.xticks([0, 4, 8, 12, 16, 20])
plt.yticks([-5, -10, -15])
fig.supxlabel('Epochs ($\\times 1K$)')
fig.supylabel('Episodic Reward')
fig.tight_layout()
plt.subplots_adjust(bottom=0.23, hspace=0.6, wspace=0.16, left=0.15)

plt.fill_between([0, 4], -19, -16, color=f'C0', alpha=0.5)
plt.fill_between([4, 16], -19, -16, color=f'C1', alpha=0.5)
plt.fill_between([16, 20], -19, -16, color=f'C0', alpha=0.5)
plt.text(0.3, -18.2, f'No Trap', color='k', fontsize=8, zorder=20)
plt.text(8, -18.2, f'Trap Active', color='k', fontsize=8, zorder=20)
plt.text(16.3, -18.2, f'No Trap', color='k', fontsize=8, zorder=20)

plt.savefig('figures/grid_reward_time_series.pdf', format='pdf')

fig, ax = plt.subplots(1, 1, figsize=(3.25, 1.5))

for dfi, label, color, lst in zip([0, 1, 2], bases, ['C3', 'C9', 'C2'], ['--', ':', '-']):
    df = df_list[dfi]
    st = df['time'].max() // 1000
    df['tint'] = (df['time'] / st).astype(int)
    rew = 1 - df.groupby('tint').mean()['pi_0']
    rew_up = 1 - df.groupby('tint').min()['pi_0']
    rew_dn = 1 - df.groupby('tint').max()['pi_0']
    tint = df.groupby('tint').mean().reset_index()['tint'] * st / 1000

    ax.plot(tint, rew, label=label, color=color, linestyle=lst)
    ax.fill_between(tint, rew_up, rew_dn, color=color, alpha=0.1, linestyle=lst)

ax.grid()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False)

ax.legend(loc='center')
plt.ylim(top=1.05, bottom=-0.3)
plt.xticks([0, 4, 8, 12, 16, 20])
plt.yticks([0, 0.25, 0.5, 0.75, 1.0])
fig.supxlabel('Epochs ($\\times 1K$)')
fig.supylabel(r'$D_{TV}(\pi({z=\text{No Trap} \over {s=\text{Blue Cell}}}), \pi_{opt})$')
fig.tight_layout()
plt.subplots_adjust(bottom=0.23, hspace=0.6, wspace=0.16, left=0.19)

plt.fill_between([0, 4], -0.25, -0.05, color=f'C0', alpha=0.5)
plt.fill_between([4, 16], -0.25, -0.05, color=f'C1', alpha=0.5)
plt.fill_between([16, 20], -0.25, -0.05, color=f'C0', alpha=0.5)
plt.text(0.3, -0.20, f'No Trap', color='k', fontsize=8, zorder=20)
plt.text(8, -0.20, f'Trap Active', color='k', fontsize=8, zorder=20)
plt.text(16.3, -0.20, f'No Trap', color='k', fontsize=8, zorder=20)

plt.savefig('figures/grid_pol_0_time_series.pdf', format='pdf')

fig, ax = plt.subplots(1, 1, figsize=(3.25, 1.5))

for dfi, label, color, lst in zip([0, 1, 2], bases, ['C3', 'C9', 'C2'], ['--', ':', '-']):
    df = df_list[dfi]
    st = df['time'].max() // 1000
    df['tint'] = (df['time'] / st).astype(int)
    rew = 1 - df.groupby('tint').mean()['pi_1']
    rew_up = 1 - df.groupby('tint').min()['pi_1']
    rew_dn = 1 - df.groupby('tint').max()['pi_1']
    tint = df.groupby('tint').mean().reset_index()['tint'] * st / 1000

    ax.plot(tint, rew, label=label, color=color, linestyle=lst)
    ax.fill_between(tint, rew_up, rew_dn, color=color, alpha=0.1, linestyle=lst)

ax.grid()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False)

ax.legend(loc='center')
plt.ylim(top=1.05, bottom=-0.3)
plt.xticks([0, 4, 8, 12, 16, 20])
plt.yticks([0, 0.25, 0.5, 0.75, 1.0])
fig.supxlabel('Epochs ($\\times 1K$)')
fig.supylabel(r'$D_{TV}(\pi({z=\text{Trap Active} \over {s=\text{Blue Cell}}}), \pi_{opt})$')
fig.tight_layout()
plt.subplots_adjust(bottom=0.23, hspace=0.6, wspace=0.16, left=0.19)

plt.fill_between([0, 4], -0.25, -0.05, color=f'C0', alpha=0.5)
plt.fill_between([4, 16], -0.25, -0.05, color=f'C1', alpha=0.5)
plt.fill_between([16, 20], -0.25, -0.05, color=f'C0', alpha=0.5)
plt.text(0.3, -0.20, f'No Trap', color='k', fontsize=8, zorder=20)
plt.text(8, -0.20, f'Trap Active', color='k', fontsize=8, zorder=20)
plt.text(16.3, -0.20, f'No Trap', color='k', fontsize=8, zorder=20)

plt.savefig('figures/grid_pol_1_time_series.pdf', format='pdf')
