import pandas as pd
import os


def load_data(path: str, df_dict: dict) -> dict:
    for raw_file in ['u.data', 'u.genre', 'u.info', 'u.item', 'u.occupation', 'u.user']:
        with open(path + "\\" + raw_file, mode='r') as file:
            df_dict[raw_file[2:]] = file.read()
    return df_dict


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

    df_merged_movie_data = pd.DataFrame()
    for df in df_dict_map.values():
        df_merged_movie_data: pd.DataFrame = pd.merge(df_merged_movie_data, df, on='movieId')
