import numpy as np
import pandas as pd

from params_monte_carlo import (
    estimates_dir,
    methods,
    methods_dic,
    method_files,
    headers_demand,
    data_dir,
    var_xi_vals,
    sigma2_vals,
    gamma_vals,
    var_omega_vals,
)


def read_results_method(params, method):
    sigma2, gamma_val, var_xi, var_omega = params
    pm_dir = estimates_dir / f"est_s{sigma2}_g{gamma_val}_x{var_xi}_w{var_omega}"
    headers, str_method = methods_dic[method]
    file = method_files[method]
    df = pd.read_csv(pm_dir / (file + ".csv"))
    if df.columns[0] == "V1":  # no headers in combinedMPECest.csv
        df.columns = headers_demand
    # print(df.head())
    df_full = pd.DataFrame()
    df_full["Simul"] = np.arange(len(df))
    df_full["Method"] = str_method
    df_full["sigma2"] = sigma2
    df_full["gamma"] = gamma_val
    df_full["var_xi"] = var_xi
    df_full["var_omega"] = var_omega
    for i, var in enumerate(headers):
        df_full[var] = df.iloc[:, i]
    # confusion on sign of betap
    if "beta_p" in df_full.columns:
        df_full["beta_p"] = -df_full["beta_p"]
    # make variances into shares
    if "V_1" in df_full.columns:
        v_total = df_full["V_1"] + df_full["V_2"] + df_full["V_3"]
        df_full["V_1"] /= v_total
        df_full["V_2"] /= v_total
        df_full["V_3"] /= v_total
    if "VV_1" in df_full.columns:
        vv_total = df_full["VV_1"] + df_full["VV_2"] + df_full["VV_3"]
        df_full["VV_1"] /= vv_total
        df_full["VV_2"] /= vv_total
        df_full["VV_3"] /= vv_total

    df_melted = pd.melt(
        df_full,
        id_vars=["Method", "sigma2", "gamma", "var_xi", "var_omega"],
        value_vars=headers,
        var_name="Parameter",
        value_name="Estimate",
    )
    return df_melted


def read_results(params):
    df_methods = [read_results_method(params, method) for method in methods]
    df = pd.concat(df_methods)
    return df


if __name__ == "__main__":
    df_list = []
    for var_xi in var_xi_vals:
        for var_omega in var_omega_vals:
            for sigma2 in sigma2_vals:
                for gamma_val in gamma_vals:
                    params = (sigma2, gamma_val, var_xi, var_omega)
                    df_list.append(read_results(params))
    df_results = pd.concat(df_list)

    df_results.to_pickle(f"{data_dir}/df_results.pkl")
