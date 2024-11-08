import pandas as pd
import os


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
    df_dict['item'].drop(['video_release_date'], inplace=True, axis=1)
    df_dict['item']['release_date'] = pd.to_datetime(df_dict['item']['release_date'], format='%d-%b-%Y')
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


def get_cat_cols(df: pd.DataFrame) -> list:
    input_variables: list = []
    for col in df.columns:
        if df[col].dtype not in ['float64', 'int64']:
            input_variables.append(col)
    return input_variables


def print_results_to_csv(data_structure, path: str, file_name: str, categories: list) -> None:
    if type(data_structure) is pd.DataFrame:
        data_structure.to_csv(os.path.join(path, f'{file_name}.csv'))
    if type(data_structure) is dict:
        for data in data_structure.keys():
            for df, cat in zip(data_structure[data], categories):
                df.to_csv(os.path.join(path, f'{file_name}_{data}_{cat}.csv'))
    else:
        data = pd.DataFrame(data_structure)
        data.to_csv(os.path.join(path, f'{file_name}.csv'))
