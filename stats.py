import os
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Tuple

from utils import *


def stat_numeric_variables(df: pd.DataFrame, save_dir: str) -> Tuple[List[str], pd.DataFrame]:
    num_cols = get_numeric_cols(df)

    num_var_stats: dict = {
        'mean': [],
        'median': [],
        'std_dev': [],
        'skewness': [],
        'kurtosis': []
    }

    summaries = []

    for col in num_cols:
        summaries.append(df[col].describe())
        num_var_stats['mean'].append(df[col].mean())
        num_var_stats['median'].append(df[col].median())
        num_var_stats['std_dev'].append(df[col].std())
        num_var_stats['skewness'].append(df[col].skew())
        num_var_stats['kurtosis'].append(df[col].kurt())

        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        sns.histplot(df[col], kde=True)
        plt.title(f'{col} histogram')

        plt.subplot(1, 2, 2)
        sns.boxplot(x=df[col])
        plt.title(f'{col} Boxplot')

        plot_filename = os.path.join(save_dir, f'{col}_plot.png')
        if os.path.exists(plot_filename):
            os.remove(plot_filename)
        plt.savefig(plot_filename)
        plt.close()

    return summaries, pd.DataFrame(num_var_stats)


def stat_categorical_variables(df: pd.DataFrame, save_dir: str) -> list:
    cat_cols = get_cat_cols(df)
    list_drop_cats = ['timestamp', 'zip_code', 'IMDb_URL', 'release_date', 'movie_title', 'zip_code']
    cat_cols = [col for col in cat_cols if col not in list_drop_cats]
    freq_tables = []

    for col in cat_cols:
        freq_tables.append(df[col].value_counts())

        plt.figure(figsize=(6, 4))
        sns.countplot(x=col, data=df)
        plt.title(f'Frequency of {col}')
        plt.xticks(rotation=90)

        plot_filename = os.path.join(save_dir, f'{col}_plot.png')
        if os.path.exists(plot_filename):
            os.remove(plot_filename)
        plt.savefig(plot_filename)
        plt.close()

    return freq_tables


def stat_cat_num_combination(df: pd.DataFrame, categories: list, num_vars: list, save_dir: str):
    results: dict = {
        'mean': [],
        'median': [],
        'std_dev': [],
    }

    for cat in categories:
        df_for_cat = df[[cat] + num_vars]
        results['mean'].append(df_for_cat.groupby(by=[cat]).mean())
        results['median'].append(df_for_cat.groupby(by=[cat]).median())
        results['std_dev'].append(df_for_cat.groupby(by=[cat]).std())

    return results
