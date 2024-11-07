import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(path: str, df_dict: dict) -> dict:
    sep_and_colnames_map: dict = {
        'u.data': ['\t', ['user_id', 'item_id', 'rating', 'timestamp']],
        'u.genre': ['|', ['genre', 'genre_id']],
        'u.info': [',', ['info']],
        'u.item': ['|', ['item_id', 'movie_title', 'release_date', 'video_release_date',
                         'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
                         'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                         'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                         'Thriller', 'War', 'Western']],
        'u.occupation': [',', ['occupation']],
        'u.user': ['|', ['user_id', 'age', 'gender', 'occupation', 'zip_code']],
    }
    for raw_file in ['u.data', 'u.genre', 'u.info', 'u.item', 'u.occupation', 'u.user']:
        df_dict[raw_file[2:]] = pd.read_csv(path + "\\" + raw_file,
                                            sep=sep_and_colnames_map[raw_file][0],
                                            encoding='latin-1',
                                            header=None,
                                            names=sep_and_colnames_map[raw_file][1])
    df_dict['data']['timestamp'] = pd.to_datetime(df_dict['data']['timestamp'], unit='s')
    return df_dict


def merge_data(df_dict: dict) -> pd.DataFrame:
    df = pd.merge(df_dict['data'], df_dict['user'], on='user_id')
    df = pd.merge(df, df_dict['item'], on='item_id')
    return df


def get_numeric_cols(df: pd.DataFrame) -> list:
    input_variables: list = []
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64'] and not df[col].nunique() == 2:
            input_variables.append(col)
    return input_variables


def stat_numeric_variables(df: pd.DataFrame, save_dir: str) -> None:
    num_cols = get_numeric_cols(df)

    num_var_stats: dict = {
        'mean': [],
        'median': [],
        'std_dev': [],
        'skewness': [],
        'kurtosis': []
    }

    for col in num_cols:
        summary = df[col].describe()
        num_var_stats['mean'].append(df[col].mean())
        num_var_stats['median'].append(df[col].median())
        num_var_stats['std_dev'].append(df[col].std())
        num_var_stats['skewness'].append(df[col].skew())
        num_var_stats['kurtosis'].append(df[col].kurt())

        print(summary)

        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        sns.histplot(df[col], kde=True)
        plt.title(f'{col} histogram')

        plt.subplot(1, 2, 2)
        sns.boxplot(x=df[col])
        plt.title(f'{col} Boxplot')

        plot_filename = os.path.join(save_dir, f'{col}_plot.png')
        plt.savefig(plot_filename)
        plt.close()


def stat_categorical_variables(df: pd.DataFrame, save_dir: str) -> None:
    pass

if __name__ == '__main__':
    df_dict_map: dict = {
        'data': pd.DataFrame(),
        'genre': pd.DataFrame(),
        'info': pd.DataFrame(),
        'item': pd.DataFrame(),
        'occupation': pd.DataFrame(),
        'user': pd.DataFrame(),
    }
    df_dict_map: dict = load_data(os.path.join(os.getcwd(), "data"), df_dict_map)
    df_movie_rating_data: pd.DataFrame = merge_data(df_dict_map)

    stat_numeric_variables(df_movie_rating_data, os.path.join(os.getcwd(), "plots"))

    stat_categorical_variables(df_movie_rating_data, os.path.join(os.getcwd(), "plots"))

