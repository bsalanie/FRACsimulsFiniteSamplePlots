""" plotting the densities of the estimates, Seaborn version"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from bsutils import mkdir_if_needed

from params_monte_carlo import *

sns.set_context("paper")
sns.set_style("whitegrid")


def select_data(df, subcase, coeff_subset):
    """extract the results for a subcase and a subset of parameters"""
    sigma2, gamma_val, var_xi, var_omega = subcase
    crit1 = df["sigma2"] == sigma2
    crit2 = df["var_xi"] == var_xi
    crit3 = df["var_omega"] == var_omega
    crit4 = df["gamma"] == gamma_val
    sel_cond = crit1 & crit2 & crit3 & crit4
    if coeff_subset == "All":
        select_df = df[sel_cond]
    else:
        str_coeffs, methods_coeffs = coeff_subsets[coeff_subset]
        crit5 = df["Parameter"].isin(str_coeffs)
        crit6 = df["Method"].isin(methods_coeffs)
        select_df = df[sel_cond & crit5 & crit6]
    return select_df


def plot_estimates(df, subcase, coeff_subset, true_vals, savedir):
    """plots densities of a subset of estimates for a subcase"""
    select_df = select_data(df, subcase, coeff_subset)
    n_coeffs = len(coeff_subsets[coeff_subset][0])
    sigma2, gamma_val, var_xi, var_omega = subcase

    d = {"ls": ["-", "--", "-.", ":"]}

    g = sns.FacetGrid(
        select_df,
        col="Parameter",
        col_wrap=3,
        hue="Method",
        hue_kws=d,
        sharex=False,
        margin_titles=True,
    )
    g.map(sns.kdeplot, "Estimate")
    g.set_titles(col_template="{col_name}")

    if (
        "variance_shares" not in coeff_subset
    ):  # we add vertical lines for the true values
        # dict of line positions
        lines_true = {}
        for i in range(n_coeffs):
            lines_true[i] = true_vals[i]
        # flatten axes into a 1-d array
        axes = g.axes.flatten()
        # iterate through the axes to add line  to each plot
        for i, ax in enumerate(axes):
            ax.axvline(lines_true[i], ls="--", c="purple")
            # ax.set_xlim(xlims[icol])
    else:
        # flatten axes into a 1-d array
        axes = g.axes.flatten()
        # iterate through the axes to add [0, 1] x range  to each plot
        for i, ax in enumerate(axes):
            ax.set_xlim((0.0, 1.0))

    g.set(yticks=[], xlabel="")  # set y ticks to blank
    g.despine(left=True)  # remove 'spines'

    # g.fig.subplots_adjust(top=0.85)
    g.fig.suptitle(
        "For "
        + r"$\sigma^2=$"
        + f"{sigma2}, "
        + r"$\sigma_\xi^2=$"
        + f"{var_xi}, "
        + r"$\gamma=$"
        + f"{gamma_val}, "
        + r"$\sigma_\omega^2=$"
        + f"{var_omega}",
        y=1.03,
    )

    g.add_legend()

    savedir = mkdir_if_needed(savedir)

    g.savefig(
        f"{savedir}/{coeff_subset}_s{sigma2}_o{var_omega}_x{var_xi}_g{gamma_val}.png"
    )
    plt.clf()


if __name__ == "__main__":

    sns.set_style("whitegrid")
    sns.set_context("paper")

    df_results = pd.read_pickle(f"{data_dir}/df_results.pkl")
    # make pretty LaTeX names
    df_results["Parameter"] = df_results["Parameter"].map(
        {k: v for (k, v) in zip(headers_coeffs, str_coeffs)}
    )

    for gamma_val in gamma_vals:
        for var_omega in var_omega_vals:
            for var_xi in var_xi_vals:
                for sigma2 in sigma2_vals:
                    subcase = (sigma2, gamma_val, var_xi, var_omega)
                    print(subcase)
                    # plots for the mean coefficients of demand
                    true_vals = [basic_values[j] for j in headers_demand_betas]
                    plot_estimates(
                        df_results,
                        subcase,
                        "means_betas",
                        true_vals,
                        plots_dir / "plots_means_betas",
                    )
                    # plots for the variances of the coefficients of demand
                    true_vals = [
                        basic_values[j] * sigma2 / basic_values["var_1"]
                        for j in headers_demand_sigmas
                    ]
                    plot_estimates(
                        df_results,
                        subcase,
                        "variances_betas",
                        true_vals,
                        plots_dir / "plots_variances_betas",
                    )
                    # plots for the coefficients of supply
                    true_vals = [basic_values["gamma_0"]] + [
                        basic_values[j] * gamma_val / basic_values["gamma_1"]
                        for j in headers_supply[1:]
                    ]
                    plot_estimates(
                        df_results,
                        subcase,
                        "gammas",
                        true_vals,
                        plots_dir / "plots_gammas",
                    )
                    # plots for the variance shares of demand
                    true_vals = [basic_values[j] for j in headers_varianceshares_demand]
                    plot_estimates(
                        df_results,
                        subcase,
                        "variance_shares_demand",
                        true_vals,
                        plots_dir / "plots_variance_shares",
                    )
                    # plots for the variance shares of supply
                    true_vals = [basic_values[j] for j in headers_varianceshares_supply]
                    plot_estimates(
                        df_results,
                        subcase,
                        "variance_shares_supply",
                        true_vals,
                        plots_dir / "plots_variance_shares",
                    )
