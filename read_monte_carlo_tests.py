import numpy as np
import pandas as pd

from params_monte_carlo import (
    estimates_dir,
    methods_dic,
    test_methods,
    data_dir,
    testo_dic,
    testp_dic,
    test1_dic,
    test_beta_1_configs,
    test_var_1_configs,
    test_var_p_configs,
    test_joint_1_configs,
    test_over_ident_configs,
)


def read_resus_(params, method, test_dic):
    true_beta_1, true_var_1, true_var_p = params
    pm_dir = estimates_dir / f"est_b1{true_beta_1}_s1{true_var_1}_sp{true_var_p}"
    file_tests = test_dic[method]
    # print(f"Reading {pm_dir / (file_tests + '.csv')}")
    df_tests = pd.read_csv(pm_dir / (file_tests + ".csv"))
    # print(f"{df_tests.columns=}")
    return df_tests


def read_beta_1(params, method, test_dic):
    true_beta_1 = params[0]
    df_1 = read_resus_(params, method, test_dic)
    df_full = pd.DataFrame()
    df_full["Simul"] = np.arange(len(df_1))
    df_full["Method"] = methods_dic[method][1]
    df_full["true_beta_1"] = true_beta_1
    df_full["estimated_beta_1"] = df_1["beta_1"]
    df_full["test_stat"] = df_1["t_stat_1"]
    df_full["p_value"] = df_1["p_value_1"]

    df_melted = pd.melt(
        df_full,
        id_vars=["Method", "true_beta_1"],
        value_vars=["estimated_beta_1", "test_stat", "p_value"],
        var_name="Parameter",
        value_name="Value",
    )
    return df_melted


def read_var_1(params, method, test_dic):
    true_var_1 = params[1]
    df_1 = read_resus_(params, method, test_dic)
    df_full = pd.DataFrame()
    df_full["Simul"] = np.arange(len(df_1))
    df_full["Method"] = methods_dic[method][1]
    df_full["true_var_1"] = true_var_1
    df_full["estimated_var_1"] = df_1["var_1"]
    df_full["test_stat"] = df_1["t_stat_2"]
    df_full["p_value"] = df_1["p_value_2"]

    df_melted = pd.melt(
        df_full,
        id_vars=["Method", "true_var_1"],
        value_vars=["estimated_var_1", "test_stat", "p_value"],
        var_name="Parameter",
        value_name="Value",
    )
    return df_melted


def read_joint_1(params, method, test_dic):
    true_beta_1, true_var_1, _ = params
    df_1 = read_resus_(params, method, test_dic)
    df_full = pd.DataFrame()
    df_full["Simul"] = np.arange(len(df_1))
    df_full["Method"] = methods_dic[method][1]
    df_full["true_beta_1"] = true_beta_1
    df_full["estimated_beta_1"] = df_1.iloc[:, 1]
    df_full["true_var_1"] = true_var_1
    df_full["estimated_var_1"] = df_1["var_1"]
    df_full["test_stat_both"] = df_1["chi_sq_stat_3_upper"]
    # df_full["p_value_lower"] = df_1[""]
    df_full["p_value"] = df_1["p_value_3_upper"]

    df_melted = pd.melt(
        df_full,
        id_vars=["Method", "true_beta_1", "true_var_1"],
        value_vars=["estimated_beta_1", "estimated_var_1", "test_stat_both", "p_value"],
        var_name="Parameter",
        value_name="Value",
    )
    # print(df_melted)
    return df_melted


def read_var_p(params, method, test_dic):
    true_var_p = params[2]
    df_p = read_resus_(params, method, test_dic)
    df_full = pd.DataFrame()
    df_full["Simul"] = np.arange(len(df_p))
    df_full["Method"] = methods_dic[method][1]
    df_full["true_var_p"] = true_var_p
    df_full["estimated_var_p"] = df_p["var_p"]
    df_full["test_stat"] = df_p["t_stat_1"]
    df_full["p_value"] = df_p["p_value_1"]

    df_melted = pd.melt(
        df_full,
        id_vars=["Method", "true_var_p"],
        value_vars=["estimated_var_p", "test_stat", "p_value"],
        var_name="Parameter",
        value_name="Value",
    )
    return df_melted


def read_over_ident(params, method, test_dic):
    df_o = read_resus_(params, method, test_dic)
    df_full = pd.DataFrame()
    df_full["Simul"] = np.arange(len(df_o))
    df_full["Method"] = methods_dic[method][1]
    df_full["test_stat"] = df_o["over_id_chi_sq"]
    df_full["p_value"] = df_o["p_value_over_id"]

    df_melted = pd.melt(
        df_full,
        id_vars=["Method"],
        value_vars=["test_stat", "p_value"],
        var_name="Parameter",
        value_name="Value",
    )
    return df_melted


def store_results(read_function, configs, savefile, test_dic):
    df_list = []
    for params in configs:
        df_methods = [
            read_function(params, method, test_dic) for method in test_methods
        ]
        df = pd.concat(df_methods)
        df_list.append(df)
    df_results = pd.concat(df_list)
    df_results.to_pickle(f"{data_dir}/{savefile}.pkl")
    return df_results


if __name__ == "__main__":

    df_beta_1_results = store_results(
        read_beta_1, test_beta_1_configs, "df_test_beta_1_results", test1_dic
    )
    df_var_1_results = store_results(
        read_var_1, test_var_1_configs, "df_test_var_1_results", test1_dic
    )
    df_joint_1_results = store_results(
        read_joint_1, test_joint_1_configs, "df_test_joint_1_results", test1_dic
    )
    df_var_p_results = store_results(
        read_var_p, test_var_p_configs, "df_test_var_p_results", testp_dic
    )
    df_over_ident_results = store_results(
        read_over_ident,
        test_over_ident_configs,
        "df_test_over_ident_results",
        testo_dic,
    )
