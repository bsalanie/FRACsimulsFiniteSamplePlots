""" parameters of the simulations """

from pathlib import Path
from bsutils import mkdir_if_needed


frank_blp_root = Path.home() / "Dropbox/BernardFrankBLP"
monte_carlo_dir = mkdir_if_needed(
    frank_blp_root / "Q2-2022" / "Estimates_and_Tests_May_29"
)
estimates_dir = monte_carlo_dir / "estimates"
data_dir = mkdir_if_needed("./Latest_Data")
plots_dir = mkdir_if_needed("./Latest_Plots")

var_omega_vals = (0.2,)
var_omega_strs = tuple(map(str, var_omega_vals))
var_xi_vals = (0.5, 1)
var_xi_strs = tuple(map(str, var_xi_vals))
sigma2_vals = (0.2, 0.5, 1)
sigma2_strs = tuple(map(str, sigma2_vals))
gamma_vals = (0.1, 0.2)
gamma_strs = tuple(map(str, gamma_vals))

headers_demand_betas = ["beta_0", "beta_1", "beta_2", "beta_3", "beta_p"]
str_demand_betas = [
    r"$\beta_0$",
    r"$\beta_1$",
    r"$\beta_2$",
    r"$\beta_3$",
    r"$\beta_p$",
]
headers_demand_sigmas = ["var_1", "var_2", "var_3", "var_p"]
str_demand_sigmas = [r"$\sigma_1^2$", r"$\sigma^2_2$", r"$\sigma^2_3$", r"$\sigma_p^2$"]
headers_demand = headers_demand_betas + headers_demand_sigmas
str_demand = str_demand_betas + str_demand_sigmas

headers_varianceshares_demand = ["V_1", "V_2", "V_3"]
str_varianceshares_demand = [r"$V^D_1$", r"$V^D_2$", r"$V^D_3$"]

headers_supply = ["gamma_0", "gamma_1", "gamma_2", "gamma_3"]
str_supply = [r"$\gamma_0$", r"$\gamma_1$", r"$\gamma_2$", r"$\gamma_3$"]

headers_varianceshares_supply = ["VV_1", "VV_2", "VV_3"]
str_varianceshares_supply = [r"$V^S_1$", r"$V^S_2$", r"$V^S_3$"]
str_varianceshares = str_varianceshares_demand + str_varianceshares_supply
headers_varianceshares = headers_varianceshares_demand + headers_varianceshares_supply


headers_DandS = headers_demand + headers_supply
str_DandS = str_demand + str_supply

headers_coeffs = (
    headers_demand
    + headers_varianceshares_demand
    + headers_supply
    + headers_varianceshares_supply
)
str_coeffs = (
    str_demand + str_varianceshares_demand + str_supply + str_varianceshares_supply
)

methods = ["MPEC", "2SIV", "BIAS_2SIV", "SUPPLY", "3SLS"]
list_headers = [
    headers_demand,
    headers_demand + headers_varianceshares_demand,
    headers_demand,
    headers_supply + headers_varianceshares_supply,
    headers_DandS,
]
list_str_methods = ["MPEC", "FRAC(D)", "Corrected", "FRAC(S)", "3SLS"]
methods_dic = dict(zip(methods, list(zip(list_headers, list_str_methods))))

# define useful subsets of coefficients, with pretty LaTeX names and methods where they appear
methods_demand = ["MPEC", "FRAC(D)", "Corrected", "3SLS"]
methods_supply = ["FRAC(S)", "3SLS"]
methods_varianceshares_demand = ["FRAC(D)"]
methods_varianceshares_supply = ["FRAC(S)"]
coeff_subsets = {
    "All": str_coeffs,
    "means_betas": (str_demand_betas, methods_demand),
    "variances_betas": (str_demand_sigmas, methods_demand),
    "gammas": (str_supply, methods_supply),
    "variance_shares_demand": (
        str_varianceshares_demand,
        methods_varianceshares_demand,
    ),
    "variance_shares_supply": (
        str_varianceshares_supply,
        methods_varianceshares_supply,
    ),
}


method_files = {"MPEC": "combined_MPECest"}
for method in methods[1:]:
    method_files[method] = f"rho0_{method}_neg_abs"

# basic_values are the true values for gamma_val = 0.1
#     and sigma2_val = 0.5
#  for other values of gamma_val we multiply (gamma1, gamma2, gamma3)
#     by gamma_val/0.1
#  for other values of sigma2_val we multiply all sigmaX_2
#     by sigma2_val/0.5

basic_values = {
    "beta_0": 7.0,
    "beta_1": 1.5,
    "beta_2": 1.5,
    "beta_3": 0.5,
    "beta_p": 4.0,
    "var_1": 0.5,
    "var_2": 0.5,
    "var_3": 0.5,
    "var_p": 0.25,
    "gamma_0": 0.5,
    "gamma_1": 0.1,
    "gamma_2": -0.1,
    "gamma_3": -0.1,
    # fake true values
    "V_1": 0.0,
    "V_2": 0.0,
    "V_3": 0.0,
    "VV_1": 0.0,
    "VV_2": 0.0,
    "VV_3": 0.0,
}


# test_configs: values for beta_1, var_1, and var_p
test_configs = [
    [0, 0, 0.25],
    [0, 0.1, 0.25],
    [0, 0.2, 0.25],
    [0, 0.5, 0.25],
    [0.25, 0, 0.25],
    [0.75, 0, 0.25],
    [1.5, 0, 0.25],
    [1.5, 0.1, 0.25],
    [1.5, 0.2, 0.25],
    [1.5, 0.5, 0],
    [1.5, 0.5, 0.05],
    [1.5, 0.5, 0.1],
    [1.5, 0.5, 0.25],  # true values
]

test_beta_1_configs = [test_configs[0]] + test_configs[4:7]
test_var_1_configs = test_configs[6:9] + [test_configs[-1]]
test_joint_1_configs = test_configs[:7]
test_var_p_configs = test_configs[-4:]

# we only do the overidentification test for the true values
test_over_ident_configs = [test_configs[-1]]

test_methods = ["2SIV", "BIAS_2SIV"]
test1_files = ["beta_sig_1_hyp_" + method for method in test_methods]
test1_dic = dict(zip(test_methods, test1_files))
testp_files = ["sigma_p_hyp_" + method for method in test_methods]
testp_dic = dict(zip(test_methods, testp_files))
testo_files = test1_files
testo_dic = dict(zip(test_methods, testo_files))
