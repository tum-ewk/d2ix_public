import message_ix
import pandas as pd


def create_plotdata_df(results: message_ix.Scenario) -> pd.DataFrame:
    df = pd.DataFrame()
    for var in ['ACT', 'CAP', 'CAP_NEW']:
        _df = group_data(var, results)
        df = df.append(_df)
    return df


def group_data(var: str, results: message_ix.Scenario) -> pd.DataFrame:
    # TODO: add as variable
    units = {'ACT': 'GWa/a', 'CAP': 'GW', 'CAP_NEW': 'GW/a', 'EMISS': 'MtCO2/a'}
    historicals = {'ACT': 'historical_activity', 'CAP_NEW': 'historical_new_capacity'}
    df = results.var(var)
    df = df.loc[df.lvl != 0]

    if var in historicals:
        df_hist = results.par(historicals[var])
        df_hist = df_hist.rename(columns={'value': 'lvl'})
        df_hist = df_hist.loc[df_hist.lvl != 0]
        df = df.append(df_hist, sort=False)

    # group Variable by technology and reshape to timeseries format
    if 'year_act' in df.columns:
        df = df[['node_loc', 'technology', 'year_act', 'lvl']]
        df = df.groupby(['node_loc', 'year_act', 'technology'],
                        as_index=False).sum().copy()
        df = df.rename(columns={'node_loc': 'node', 'year_act': 'year'})

    elif var == 'EMISS':
        df_hist = results.par('historical_emission')
        df_hist = df_hist.rename(columns={'type_emission': 'emission', 'type_year': 'year', 'value': 'lvl'})
        df_hist = df_hist.loc[df_hist.lvl != 0]
        df = df.append(df_hist, sort=False)
        df['year'] = df.year.astype(int)

        df = df[['node', 'emission', 'year', 'lvl']]
        df = df.groupby(['node', 'year', 'emission'], as_index=False).sum().copy()
    else:
        df = df[['node_loc', 'technology', 'year_vtg', 'lvl']]
        df = df.groupby(['node_loc', 'year_vtg', 'technology'], as_index=False).sum().copy()
        df = df.rename(columns={'node_loc': 'node', 'year_vtg': 'year'})

    df['unit'] = units[var]
    df['variable'] = var

    return df


def extract_synonyms_colors(data: pd.DataFrame) -> dict:
    post_data = {}
    _tmp = data[['technology', 'synonym']]
    _tmp = _tmp.dropna().set_index('technology')
    _tmp = _tmp.to_dict()
    post_data['synonyms'] = _tmp['synonym']

    _tmp = data[['technology', 'color']]
    _tmp = _tmp.set_index('technology')
    _tmp = _tmp.dropna().to_dict()
    post_data['colors'] = _tmp['color']
    return post_data
