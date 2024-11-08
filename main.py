from stats import *


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

    num_var_summaries, num_stat_measures = stat_numeric_variables(df_movie_rating_data,
                                                                  os.path.join(os.getcwd(), "plots"))
    cat_stat_frequencies = stat_categorical_variables(df_movie_rating_data, os.path.join(os.getcwd(), "plots"))

    categories = ['gender', 'occupation']
    cat_num_describe: dict = stat_cat_num_combination(df=df_movie_rating_data,
                                                      categories=categories,
                                                      num_vars=get_numeric_cols(df_movie_rating_data),
                                                      save_dir=os.path.join(os.getcwd(), "plots")
                                                      )

    measures_to_csv_map = {'num_var_summaries': num_var_summaries,
                           'num_stat_measures': num_stat_measures,
                           'cat_stat_frequencies': cat_stat_frequencies,
                           'cat_num_describe': cat_num_describe}
    for measure in measures_to_csv_map.keys():
        print_results_to_csv(measures_to_csv_map[measure], os.path.join(os.getcwd(), "measures"),
                             measure,
                             categories=categories)
