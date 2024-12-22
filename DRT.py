import numpy as np
from scipy import integrate
from scipy.linalg import toeplitz
from scipy.optimize import fsolve, minimize


def runDRT(inputPath: str, outputPath: str):
    A = np.loadtxt(inputPath)

    freq = A[:, 0]
    real = A[:, 1]
    imaginary = A[:, 2]
    freq_0 = A[:, 0]
    real_0 = A[:, 1]
    imaginary_0 = A[:, 2]
    Z_exp = real_0 + 1j * imaginary_0

    # 创建下界、上界和初始值向量
    lb = np.zeros(len(freq) + 2)
    ub = np.inf * np.ones(len(freq) + 2)
    x_0 = np.ones_like(lb)

    # 提取复数的实部和虚部
    b_re = np.real(Z_exp)  # 提取实部
    b_im = np.imag(Z_exp)  # 提取虚部

    coef = 0.5

    def rbf_gaussian_4_FWHM(x):
        return np.exp(-((x) ** 2)) - 1 / 2

    def assemble_A_re(freq, epsilon):
        # Get number of frequencies
        N_freq = len(freq)

        # Define the A_re output matrices
        out_A_re_temp = np.zeros((N_freq, N_freq))
        out_A_re = np.zeros((N_freq, N_freq + 2))

        # Define vectors R and C
        R = np.zeros(N_freq)
        C = np.zeros(N_freq)

        # Compute C vector
        for iter_freq_n in range(N_freq):
            freq_n = freq[iter_freq_n]
            freq_m = freq[0]
            C[iter_freq_n] = g_i(freq_n, freq_m, epsilon)

        # Compute R vector
        for iter_freq_m in range(N_freq):
            freq_n = freq[0]
            freq_m = freq[iter_freq_m]
            R[iter_freq_m] = g_i(freq_n, freq_m, epsilon)

        # Create Toeplitz matrix
        out_A_re_temp = toeplitz(C, R)  # Returns non-symmetric Toeplitz matrix

        # First and second columns are reserved for L and R respectively
        out_A_re[:, 2:] = out_A_re_temp
        return out_A_re

    def g_i(freq_n, freq_m, epsilon):
        alpha = 2 * np.pi * freq_n / freq_m

        # Choose among positive definite RBFs
        def rbf(x):
            return np.exp(-((epsilon * x) ** 2))

        # Define the integrand function
        def integrand_g_i(x):
            return 1.0 / (1 + alpha**2 * np.exp(2 * x)) * rbf(x)

        # Integrate from -inf to +inf with relatively tight tolerances
        out_val, _ = integrate.quad(
            integrand_g_i, -np.inf, np.inf, epsrel=1e-9, epsabs=1e-9
        )
        return out_val

    def assemble_A_im(freq, epsilon):
        # Get number of frequencies
        N_freq = len(freq)

        # Define the A_im output matrices
        out_A_im_temp = np.zeros((N_freq, N_freq))
        out_A_im = np.zeros((N_freq, N_freq + 2))

        # Define vectors R and C
        R = np.zeros(N_freq)
        C = np.zeros(N_freq)

        # Compute C vector
        for iter_freq_n in range(N_freq):
            freq_n = freq[iter_freq_n]
            freq_m = freq[0]
            C[iter_freq_n] = -g_ii(freq_n, freq_m, epsilon)

        # Compute R vector
        for iter_freq_m in range(N_freq):
            freq_n = freq[0]
            freq_m = freq[iter_freq_m]
            R[iter_freq_m] = -g_ii(freq_n, freq_m, epsilon)

        # Create Toeplitz matrix
        out_A_im_temp = toeplitz(C, R)

        # First and second columns are reserved for L and R respectively
        out_A_im[:, 2:] = out_A_im_temp
        return out_A_im

    def g_ii(freq_n, freq_m, epsilon):
        alpha = 2 * np.pi * freq_n / freq_m

        # Choose among positive definite RBFs
        def rbf(x):
            return np.exp(-((epsilon * x) ** 2))

        # Define the integrand function
        def integrand_g_ii(x):
            return alpha / (1 / np.exp(x) + alpha**2 * np.exp(x)) * rbf(x)

        # Integrate from -inf to +inf
        out_val, _ = integrate.quad(
            integrand_g_ii, -np.inf, np.inf, epsrel=1e-9, epsabs=1e-9
        )
        return out_val

    def assemble_M_2(freq, epsilon):
        # Get number of frequencies
        N_freq = len(freq)

        # Initialize output matrices
        out_M = np.zeros((N_freq + 2, N_freq + 2))
        out_M_temp = np.zeros((N_freq, N_freq))

        # Initialize vectors R and C
        R = np.zeros(N_freq)
        C = np.zeros(N_freq)

        # Compute C vector
        for iter_freq_n in range(N_freq):
            freq_n = freq[iter_freq_n]
            freq_m = freq[0]
            C[iter_freq_n] = inner_prod_rbf_2(freq_n, freq_m, epsilon)

        # Compute R vector
        for iter_freq_m in range(N_freq):
            freq_n = freq[0]
            freq_m = freq[iter_freq_m]
            R[iter_freq_m] = inner_prod_rbf_2(freq_n, freq_m, epsilon)

        # Create Toeplitz matrix
        out_M_temp = toeplitz(C, R)

        # Assign to final output matrix
        out_M[2:, 2:] = out_M_temp

        return out_M

    def inner_prod_rbf_2(freq_n, freq_m, epsilon):
        a = epsilon * np.log(freq_n / freq_m)
        # Positive definite RBF
        out_IP = (
            epsilon**3
            * (3 - 6 * a**2 + a**4)
            * np.exp(-(a**2 / 2))
            * np.sqrt(np.pi / 2)
        )
        return out_IP

    def quad_format_combined(A_re, A_im, b_re, b_im, M, lambda_):
        H = 2 * ((A_re.T @ A_re + A_im.T @ A_im) + lambda_ * M)
        H = (H.T + H) / 2  # 确保对称性
        c = -2 * (b_im.T @ A_im + b_re.T @ A_re)
        return H, c

    FWHM_coef = 2 * fsolve(rbf_gaussian_4_FWHM, 1)[0]
    delta = np.mean(np.diff(np.log(1.0 / freq)))
    epsilon = coef * FWHM_coef / delta

    A_re = assemble_A_re(freq, epsilon)
    A_im = assemble_A_im(freq, epsilon)
    A_re[:, 1] = 1
    M = assemble_M_2(freq, epsilon)

    # 设置正则化参数
    lambda_ = 1e-3

    # 计算二次规划参数
    [H_combined, f_combined] = quad_format_combined(A_re, A_im, b_re, b_im, M, lambda_)

    # 使用scipy优化求解器代替MATLAB的quadprog
    x_ridge = minimize(
        lambda x: 0.5 * x.T @ H_combined @ x + f_combined.T @ x,
        x_0,  # 初始猜测值
        bounds=list(zip(lb, ub)),  # 上下界约束
        method="L-BFGS-B",
    ).x

    # 准备HMC采样器
    mu_Z_re = A_re @ x_ridge
    mu_Z_im = A_im @ x_ridge

    # 计算残差
    res_re = mu_Z_re - b_re
    res_im = mu_Z_im - b_im

    # 计算实部和虚部残差的标准差
    sigma_re_im = np.std(np.concatenate([res_re, res_im]))

    # 构建协方差矩阵的逆
    inv_V = (1 / sigma_re_im**2) * np.eye(len(freq))

    # 计算后验分布参数
    Sigma_inv = (
        (A_re.T @ inv_V @ A_re)
        + (A_im.T @ inv_V @ A_im)
        + (lambda_ / sigma_re_im**2) * M
    )
    mu_numerator = A_re.T @ inv_V @ b_re + A_im.T @ inv_V @ b_im

    # 确保数值稳定性
    Sigma_inv = (Sigma_inv + Sigma_inv.T) / 2

    def map_array_to_gamma(freq_map, freq_coll, x, epsilon):
        def rbf(y, y0):
            return np.exp(-((epsilon * (y - y0)) ** 2))

        freq_fine = freq_map
        y0 = -np.log(freq_coll)
        out_gamma = np.zeros(len(freq_map))

        # 对每个频率点进行计算
        for i in range(len(freq_map)):
            freq_map_loc = freq_map[i]
            y = -np.log(freq_map_loc)
            out_gamma[i] = np.dot(x, rbf(y, y0))

        return out_gamma, freq_fine

        # 计算时间常数的范围

    taumax = np.ceil(np.max(np.log10(1.0 / freq))) + 0.5
    taumin = np.floor(np.min(np.log10(1.0 / freq))) - 0.5

    # 生成细分的频率点
    freq_fine = np.logspace(-taumin, -taumax, 10 * len(freq))

    # 计算 gamma
    gamma_ridge_fine, freq_fine = map_array_to_gamma(
        freq_fine, freq, x_ridge[2:], epsilon
    )

    x = 1 / freq_fine
    np.savetxt(
        outputPath,
        np.column_stack((x, gamma_ridge_fine)),
        fmt="%.6e",
    )
    # gamma_ridge_fine是DRT纵坐标，1/freq_fine是横坐标

    des = "tau, gamma(tau) \n"
    with open(outputPath, "r") as file:
        content = file.read()
    with open(outputPath, "w") as file:
        file.write(des)
        file.write(content)
