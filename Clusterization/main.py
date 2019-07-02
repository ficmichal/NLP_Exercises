import lev_adr_clst as lac
import dice_adr_clst as dac
import preprocess as ppr
import calc_stats

preprocess = ppr.Preprocess('lines')
preprocess.preprocess()
original_data = preprocess.original_text_lines_dict

lev_clst = lac.LevenstheinClusterization(preprocess)
lev_clst.cluster_data()
lev_clst.save_results()

dac_clst = dac.DiceAddressClusterization(preprocess)
dac_clst.cluster_data()
dac_clst.save_results()

stats_calc = calc_stats.StatsCalculator(original_data)
stats_calc.print_result(['Levensthein', 'DiceCoefficient'])
