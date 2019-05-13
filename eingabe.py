from spacepy import pycdf
import numpy as np


def input_data_B_field():
    mms1_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_fgm_srvy/mms1_fgm_srvy_l2_20170130_v5.87.0.cdf ')
    mms2_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_fgm_srvy/mms2_fgm_srvy_l2_20170130_v5.87.0.cdf ')
    mms3_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_fgm_srvy/mms3_fgm_srvy_l2_20170130_v5.87.0.cdf ')
    mms4_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_fgm_srvy/mms4_fgm_srvy_l2_20170130_v5.87.0.cdf ')

    indexstart = 229750  # 229750
    time_start = 0.0
    dt = mms1_cdf['Epoch'][229751].timestamp() - mms1_cdf['Epoch'][229750].timestamp()
    numofpoints = 4096  # substitute: 2048
    time_end = numofpoints * dt
    time_series = np.linspace(time_start, time_end, numofpoints)

    offset1 = 0
    offset2 = -55
    offset3 = 6
    offset4 = -45
    sampled_data = list()

    mms1_data = mms1_cdf['mms1_fgm_b_gse_srvy_l2'][indexstart + offset1:indexstart + offset1 + numofpoints]
    mms1_data = np.delete(mms1_data, -1, axis=1)
    sampled_data.append(mms1_data)

    mms2_data = mms2_cdf['mms2_fgm_b_gse_srvy_l2'][indexstart + offset2:indexstart + offset2 + numofpoints]
    mms2_data = np.delete(mms2_data, -1, axis=1)
    sampled_data.append(mms2_data)

    mms3_data = mms3_cdf['mms3_fgm_b_gse_srvy_l2'][indexstart + offset3:indexstart + offset3 + numofpoints]
    mms3_data = np.delete(mms3_data, -1, axis=1)
    sampled_data.append(mms3_data)

    mms4_data = mms4_cdf['mms4_fgm_b_gse_srvy_l2'][indexstart + offset4:indexstart + offset4 + numofpoints]
    mms4_data = np.delete(mms4_data, -1, axis=1)
    sampled_data.append(mms4_data)

    return time_series, sampled_data


def input_data_E_field():
    mms1_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_edp_fast/mms1_edp_fast_l2_dce_20170130_v2.1.0.cdf')
    mms2_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_edp_fast/mms2_edp_fast_l2_dce_20170130_v3.0.0.cdf')
    mms3_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_edp_fast/mms3_edp_fast_l2_dce_20170130_v3.0.0.cdf')
    mms4_cdf = pycdf.CDF(
        '/Users/linrong/SpaceScience/MMSdata_n_code/MMS_edp_fast/mms4_edp_fast_l2_dce_20170130_v3.0.0.cdf')

    indexstart = 459560  # 229750
    time_start = 0.0
    dt = mms1_cdf['mms1_edp_epoch_fast_l2'][459561].timestamp() - mms1_cdf['mms1_edp_epoch_fast_l2'][459560].timestamp()
    numofpoints = 8192  # substitute: 4096
    time_end = numofpoints * dt
    time_series = np.linspace(time_start, time_end, numofpoints)

    offset1 = 1
    offset2 = 17
    offset3 = 44
    offset4 = 5
    sampled_data = list()

    mms1_data = mms1_cdf['mms1_edp_dce_gse_fast_l2'][indexstart + offset1:indexstart + offset1 + numofpoints]
    sampled_data.append(mms1_data)

    mms2_data = mms2_cdf['mms2_edp_dce_gse_fast_l2'][indexstart + offset2:indexstart + offset2 + numofpoints]
    sampled_data.append(mms2_data)

    mms3_data = mms3_cdf['mms3_edp_dce_gse_fast_l2'][indexstart + offset3:indexstart + offset3 + numofpoints]
    sampled_data.append(mms3_data)

    mms4_data = mms4_cdf['mms4_edp_dce_gse_fast_l2'][indexstart + offset4:indexstart + offset4 + numofpoints]
    sampled_data.append(mms4_data)

    return time_series, sampled_data


if __name__ == '__main__':
    t_s, s_data = input_data_E_field()
    np.save('format_E_data',s_data)
    t_s_B, s_data_B = input_data_B_field()
    np.save('format_B_data',s_data_B)
