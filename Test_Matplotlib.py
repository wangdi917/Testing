from __future__ import division
import sys
import re
import os
import copy
import random
import shutil
import math
import collections
import matplotlib
import matplotlib.pyplot as mplplt
import numpy as np
from itertools import zip_longest
# print matplotlib.__file__
# print matplotlib.__version__


# List[:-1] eliminates the last element, List[:-2] eliminates the last two elements. List[-1:] yields nothing, List[-2:] yields the last two elements.


def Block_Sensitivity_Draw(Interested_Cells_List, Final_Outputs_List, outputs_sensitivities_dict):
	cell_index = range(1, len(Interested_Cells_List)+1)
	# ['FF1', 'FF2', 'M1'], 'Overally'
	# Top_DUT.Shift1: ['0.526', '0.526', '0.158', '0.526']
	# Top_DUT.Shift2: ['0.158', '0.526', '0.000', '0.526']
	# Top_DUT.Shift3: ['0.167', '0.167', '0.167', '0.333']
	# Top_DUT.Clock1: ['0.000', '0.000', '0.167', '0.167']
	# Top_DUT.Clock2: ['0.000', '0.000', '0.167', '0.167']
	output_index = range(0, len(Final_Outputs_List))
	# FF1: ['0.526', '0.158', '0.167', '0.000', '0.000']
	# FF2: ['0.526', '0.526', '0.167', '0.000', '0.000']
	# M1: ['0.158', '0.000', '0.167', '0.167', '0.167']
	# Overally: ['0.526', '0.526', '0.333', '0.167', '0.167']
	bar_width = float(1/len(Final_Outputs_List))*0.8 # ( "%.1f" %float(1/len(Final_Outputs_List)) )
	opacity = 0.4
	sensitivity_max = 0.1
	color_list = ['b', 'y', 'g', 'r', 'c', 'm']
	#matplotlib.rcParams.update({'font.size': 22})
	mplplt.rcParams['ytick.labelsize'] = 28
	for item in Final_Outputs_List:
		block_position = Final_Outputs_List.index(item)
		color_position = block_position % len(color_list)
		block_index = [i + bar_width*block_position for i in cell_index]
		block_middle_index = [i + bar_width*int(len(cell_index)/2) for i in cell_index] # This is the middle position of the axis ticks locations.
		mplplt.bar(block_index, outputs_sensitivities_dict[item], width=bar_width, color=color_list[color_position], alpha=opacity, label=item)
		if sensitivity_max < max(outputs_sensitivities_dict[item]):
			sensitivity_max = max(outputs_sensitivities_dict[item])
		else:
			pass
	ax = mplplt.gca()
	mplplt.axis([0.75, max(block_index)+bar_width+0.25, -0.05, sensitivity_max+0.1])
	mplplt.title('Blocks Sensitivities', fontsize=28, fontweight='bold')
	mplplt.xlabel('Blocks', fontsize=24, fontweight='bold')
	mplplt.ylabel('Probability of Inducing an Error at the Probes', fontsize=28, fontweight='bold')
	mplplt.xticks(block_middle_index, Interested_Cells_List, fontsize=28, fontweight='bold', rotation=45)
	mplplt.grid(True)
	mplplt.legend()
	leg = mplplt.gca().get_legend()
	ltext = leg.get_texts()
	llines = leg.get_lines()
	frame = leg.get_frame()
	mplplt.setp(ltext, fontsize=28, fontweight='bold')
	mplplt.show()
	mplplt.close()


def Error_Persistency_Draw(Interested_Cells_List, Final_Outputs_List, outputs_sensitivities_dict):
	cell_index = range(1, len(Interested_Cells_List)+1)
	# ['FF1', 'FF2', 'M1'], 'Overally'
	# Top_DUT.Shift1: ['0.526', '0.526', '0.158', '0.526']
	# Top_DUT.Shift2: ['0.158', '0.526', '0.000', '0.526']
	# Top_DUT.Shift3: ['0.167', '0.167', '0.167', '0.333']
	# Top_DUT.Clock1: ['0.000', '0.000', '0.167', '0.167']
	# Top_DUT.Clock2: ['0.000', '0.000', '0.167', '0.167']
	output_index = range(0, len(Final_Outputs_List))
	# FF1: ['0.526', '0.158', '0.167', '0.000', '0.000']
	# FF2: ['0.526', '0.526', '0.167', '0.000', '0.000']
	# M1: ['0.158', '0.000', '0.167', '0.167', '0.167']
	# Overally: ['0.526', '0.526', '0.333', '0.167', '0.167']
	bar_width = float(1/len(Final_Outputs_List))*0.5 # ( "%.1f" %float(1/len(Final_Outputs_List)) )
	opacity = 0.4
	sensitivity_max = 0.1
	color_list = ['b', 'y', 'g', 'r', 'c', 'm']
	#matplotlib.rcParams.update({'font.size': 22})
	mplplt.rcParams['ytick.labelsize'] = 28
	for item in Final_Outputs_List:
		block_position = Final_Outputs_List.index(item)
		color_position = block_position % len(color_list)
		block_index = [i + bar_width*block_position for i in cell_index]
		block_middle_index = [i + bar_width*int(len(cell_index)/4) for i in cell_index] # This is the middle position of the axis ticks locations.
		mplplt.bar(block_index, outputs_sensitivities_dict[item], width=bar_width, color=color_list[color_position], alpha=opacity, label=item)
		if sensitivity_max < max(outputs_sensitivities_dict[item]):
			sensitivity_max = max(outputs_sensitivities_dict[item])
		else:
			pass
	ax = mplplt.gca()
	mplplt.axis([0.75, max(block_index)+bar_width+0.25, -2, sensitivity_max*1.1])
	mplplt.title('Error Persistencies', fontsize=28, fontweight='bold')
	mplplt.xlabel('Blocks', fontsize=28, fontweight='bold')
	mplplt.ylabel('Span of Induced Errors (UI)', fontsize=28, fontweight='bold')
	mplplt.xticks(block_middle_index, Interested_Cells_List, fontsize=28, fontweight='bold', rotation=45)
	mplplt.grid(True)
	mplplt.legend()
	leg = mplplt.gca().get_legend()
	ltext = leg.get_texts()
	llines = leg.get_lines()
	frame = leg.get_frame()
	mplplt.setp(ltext, fontsize=28, fontweight='bold')
	mplplt.show()
	mplplt.close()


def Stuff_Bar_Draw(Interested_Cells_List, Final_Outputs_List, outputs_sensitivities_dict):
	cell_index = range(1, len(Interested_Cells_List)+1)
	output_index = range(0, len(Final_Outputs_List))
	bar_width = float(1/len(Final_Outputs_List))*0.5 # ( "%.1f" %float(1/len(Final_Outputs_List)) )
	opacity = 0.4
	sensitivity_max = 0.1
	color_list = ['b', 'y', 'g', 'r', 'c', 'm']
	for item in Final_Outputs_List:
		block_position = Final_Outputs_List.index(item)
		color_position = block_position % len(color_list)
		block_index = [i + bar_width*block_position for i in cell_index]
		block_middle_index = [i + bar_width*int(len(cell_index)/4) for i in cell_index] # This is the middle position of the axis ticks locations.
		mplplt.bar(block_index, outputs_sensitivities_dict[item], width=bar_width, color=color_list[color_position], alpha=opacity, label=item)
		if sensitivity_max < max(outputs_sensitivities_dict[item]):
			sensitivity_max = max(outputs_sensitivities_dict[item])
		else:
			pass
	ax = mplplt.gca()
	mplplt.axis([0.75, max(block_index)+bar_width+0.25, -2, sensitivity_max*1.1])
	mplplt.title('Mitigation Strategy vs Dose Rate', fontsize=18, fontweight='bold')
	mplplt.xlabel('Dose Rate', fontsize=14, fontweight='bold')
	mplplt.ylabel('Number of Induced Errors (UI)', fontsize=14, fontweight='bold')
	mplplt.xticks(block_middle_index, Interested_Cells_List, fontsize=14, fontweight='bold', rotation=45)
	mplplt.grid(True)
	mplplt.legend()
	mplplt.show()
	mplplt.close()


def Error_Distribution_Draw(File_Record, Combined_Nets_List, error_distribution_list):
	if os.path.exists(File_Record):
		f_rec = file(File_Record, "a")
	else:
		f_rec = file(File_Record, "w")
	f_rec.write("\n\n")
	net_index = range(1, len(Combined_Nets_List)+1)
	opacity = 0.8
	color_list = ['b', 'y', 'g', 'r', 'c', 'm']
	distribution_max = 2
	for item in error_distribution_list:
	# [Top_DUT.Shift3.Inter1, Top_DUT.Shift1.Inter2, Top_DUT.Shift2.Inter2, FF1, FF2, M1]
	# [0, 6, 24, 3, 27, 0]
		if distribution_max < item:
			distribution_max = item
		else:
			pass
	mplplt.plot(net_index, error_distribution_list, alpha=opacity, linestyle='-', marker='o', markersize=10, label='Random')
	ax = mplplt.gca()
	mplplt.axis([0.75, max(net_index)+0.25, -0.5, distribution_max+2])
	mplplt.title('Error Distribution', fontsize=18, fontweight='bold')
	mplplt.xlabel('Blocks', fontsize=14, fontweight='bold')
	mplplt.ylabel('Span of Induced Errors (UI)', fontsize=14, fontweight='bold')
	mplplt.xticks(net_index, Combined_Nets_List, fontsize=10, fontweight='bold', rotation=45)
	mplplt.grid(True)
	# mplplt.legend()
	mplplt.show()
	mplplt.close()
	f_rec.close()


def Errors_Distributions_Draw(Strikes_List, Combined_Nets_List, *err_distr_lists):
	command_plotcore = ""
	command_plotall = ""
	command_legendcore = ""
	command_legendall = ""
	net_index = range(1, len(Combined_Nets_List)+1)
	color_list = ['b', 'y', 'g', 'r', 'c', 'm']
	distribution_max = 2
	for lists in err_distr_lists:
		if distribution_max < max(lists):
			distribution_max = max(lists)
		else:
			pass
		command_plotcore = command_plotcore + ("net_index, %s, " %str(lists))
	command_plotall = ("mplplt.plot( %s linestyle='-', linewidth=3, marker='o', markersize=10)" %command_plotcore)
	print ("This is the plot command core:", command_plotcore)
	#matplotlib.rcParams.update({'font.size': 22})
	mplplt.rcParams['ytick.labelsize'] = 28
	exec(command_plotall)

	for strike in Strikes_List:
		command_legendcore = command_legendcore + ("'%s', " %strike) # The names of the legends in the command must end with a ','! This is a fucking MatPlotLib rule!
	command_legendall = ("mplplt.legend((%s), loc='upper left')" %command_legendcore)
	print ("This is the legend command core:", command_legendcore)
	#matplotlib.rcParams.update({'font.size': 22})
	mplplt.rcParams['ytick.labelsize'] = 28
	exec(command_legendall)
	leg = mplplt.gca().get_legend()
	ltext = leg.get_texts()
	llines = leg.get_lines()
	frame = leg.get_frame()
	mplplt.setp(ltext, fontsize=28, fontweight='bold')
	mplplt.axis([0.75, max(net_index)+0.25, -15, distribution_max*1.1])
	mplplt.title('Error Distribution', fontsize=28, fontweight='bold')
	mplplt.xlabel('Blocks', fontsize=24, fontweight='bold')
	mplplt.ylabel('Number of Induced Errors (UI)', fontsize=28, fontweight='bold')
	mplplt.xticks(net_index, Combined_Nets_List, fontsize=28, fontweight='bold', rotation=45)
	mplplt.grid(True)
	mplplt.show()
	mplplt.close()


def Group_Bar_Draw(Interested_Cells_List, Final_Outputs_List, outputs_sensitivities_dict):
	cell_index = range(1, len(Interested_Cells_List)+1)
	output_index = range(0, len(Final_Outputs_List))
	bar_width = float(1/len(Final_Outputs_List))*0.8 # ( "%.1f" %float(1/len(Final_Outputs_List)) )
	opacity = 0.4
	sensitivity_max = 0.1
	color_list = ['b', 'y', 'g', 'r', 'c', 'm']
	#matplotlib.rcParams.update({'font.size': 22})
	#mplplt.rcParams['ytick.labelsize'] = 18
	for item in Final_Outputs_List:
		block_position = Final_Outputs_List.index(item)
		color_position = block_position % len(color_list)
		block_index = [i + bar_width*block_position for i in cell_index]
		block_middle_index = [i + bar_width*int(len(cell_index)/2) for i in cell_index] # This is the middle position of the axis ticks locations.
		mplplt.bar(block_index, outputs_sensitivities_dict[item], width=bar_width, color=color_list[color_position], alpha=opacity, label=item, log=1)
		# mplplt.yscale('symlog', linthreshy=0.01)
		if sensitivity_max < max(outputs_sensitivities_dict[item]):
			sensitivity_max = max(outputs_sensitivities_dict[item])
		else:
			pass
	ax = mplplt.gca()
	# mplplt.axis([0.75, max(block_index)+bar_width+0.25, -0.05, sensitivity_max+0.1])
	mplplt.axis([0.75, max(block_index)+bar_width+0.25, 1e-7, sensitivity_max+0.1])
	mplplt.title('Mitigation Performance', fontsize=22, fontweight='bold')
	mplplt.xlabel('Dose Rate (rad/h)', fontsize=20, fontweight='bold') # per clk cycle
	mplplt.ylabel('Bit Error Rate', fontsize=20, fontweight='bold') # Failures in Time
	mplplt.xticks(block_middle_index, Interested_Cells_List, fontsize=18, rotation=0)
	mplplt.yticks(fontsize=18, rotation=0)
	mplplt.grid(True)
	mplplt.legend()
	leg = mplplt.gca().get_legend()
	ltext = leg.get_texts()
	llines = leg.get_lines()
	frame = leg.get_frame()
	mplplt.setp(ltext, fontsize=18, fontweight='bold')
	mplplt.show()
	mplplt.close()


def Optimization_Trace_Draw(cost_list, effectiveness_list):
	overhead_list = []
	for number in cost_list:
		overhead_list.append(number/cost_list[0]*100)
	mplplt.semilogy(overhead_list, effectiveness_list, linewidth=2, linestyle='-', marker='o', markersize=10, label='Random')
	mplplt.annotate('Sol1', fontsize=18, color='g', xy=(117, 2e-6), xytext=(120, 3e-6), arrowprops=dict(facecolor='g', shrink=0.02),) # xy=(117, 0.11), xytext=(120, 0.125); xy=(117, 7e-7), xytext=(120, 13e-7)
	mplplt.annotate('Sol2', fontsize=18, color='r', xy=(144, 3.5e-7), xytext=(147, 6e-7), arrowprops=dict(facecolor='r', shrink=0.02),) # xy=(144, 0.0275), xytext=(147, 0.0325); xy=(144, 3e-7), xytext=(147, 5e-7)
	mplplt.annotate('Sol3', fontsize=18, color='c', xy=(165, 3e-7), xytext=(168, 5.5e-7), arrowprops=dict(facecolor='c', shrink=0.02),) # xy=(165, 0.0125), xytext=(168, 0.0175); xy=(165, 2.5e-7), xytext=(168, 4.5e-7)
	mplplt.axis([95, max(overhead_list)+5, min(effectiveness_list)/5, max(effectiveness_list)*5])
	mplplt.title('Trace of Optimization', fontsize=20, fontweight='bold')
	mplplt.xlabel('Overheads (%)', fontsize=18, fontweight='bold') # Numbe of Cells
	mplplt.ylabel('Bit Error Rate', fontsize=18, fontweight='bold') # Failures in Time
	mplplt.xticks(fontsize=14, rotation=0)
	mplplt.yticks(fontsize=14, rotation=0)
	mplplt.grid(True)
	# mplplt.legend()
	mplplt.show()
	mplplt.close()
def Optimization_Traces_Draw(cost_list, effectiveness_list1, effectiveness_list2, effectiveness_list3, effectiveness_list4):
	overhead_list = []
	for number in cost_list:
		overhead_list.append(number/cost_list[0]*100)
	mplplt.semilogy(overhead_list, effectiveness_list1, linewidth=2, linestyle='-', marker='o', markersize=10, label='Random')
	mplplt.semilogy(overhead_list, effectiveness_list2, linewidth=2, linestyle='-', marker='o', markersize=10, label='Random')
	mplplt.semilogy(overhead_list, effectiveness_list3, linewidth=2, linestyle='-', marker='o', markersize=10, label='Random')
	mplplt.semilogy(overhead_list, effectiveness_list4, linewidth=2, linestyle='-', marker='o', markersize=10, label='Random')
	mplplt.annotate('Sol0', fontsize=18, color='k', xy=(118, 6e-6), xytext=(122, 6e-6), arrowprops=dict(facecolor='k', shrink=0.02),)
	mplplt.annotate('Sol1', fontsize=18, color='k', xy=(102, 1.5e-7), xytext=(92, 8e-8), arrowprops=dict(facecolor='k', shrink=0.02),)
	mplplt.annotate('Sol2', fontsize=18, color='k', xy=(144, 3.5e-7), xytext=(147, 6e-7), arrowprops=dict(facecolor='k', shrink=0.02),)
	mplplt.annotate('Sol3', fontsize=18, color='k', xy=(165, 2e-7), xytext=(168, 3.5e-7), arrowprops=dict(facecolor='k', shrink=0.02),)
	mplplt.axis([90, max(overhead_list)+5, min(effectiveness_list1)/5, max(effectiveness_list1)*5])
	mplplt.title('Trace of Optimization', fontsize=20, fontweight='bold')
	mplplt.xlabel('Overheads (%)', fontsize=18, fontweight='bold') # Numbe of Cells
	mplplt.ylabel('Bit Error Rate', fontsize=18, fontweight='bold') # Failures in Time
	mplplt.xticks(fontsize=14, rotation=0)
	mplplt.yticks(fontsize=14, rotation=0)
	mplplt.grid(True)
	mplplt.legend(['DR=100krad/h', 'DR=10krad/h', 'DR=1krad/h', 'DR=100rad/h'], loc=1) # [effectiveness_list1, effectiveness_list2], 
	mplplt.show()
	mplplt.close()


def Func_Star(*args, **kwarg):
	for item in args:
		print ("List args has '%s'" %item)
	for key,value in kwarg.items():
		print ("Dictionary kwarg has '%s: %s'" %(key,value))


def f1(t):
	return np.exp(-t)*np.cos(2*np.pi*t)
def f2(t):
	return np.sin(2*np.pi*t)*np.cos(3*np.pi*t)


def Func_Probability(waiting, rate, redundancy):
	probability = (math.exp(-rate*waiting))**redundancy # In exponential distribution, rate is the amount of occurance within a time unit, waiting is the temporal length of expecting the next occurance.
	return 1-probability


def Func_Voting(impulseresp, period, redundancy):
	impulseresp_superposition = []
	for number_ind, number in enumerate(impulseresp):
		if number_ind == 0:
			impulseresp_superposition.append(number)
		else:
			probability_superposition = 0
			for residue in range(0, number_ind):
				# waiting = number_ind - residue
				probability_waiting = Func_Probability(number_ind-residue, 1/period, redundancy)
				probability_superposition = probability_superposition + number*impulseresp[residue]*probability_waiting
				print ("The product of the %dth (%.2f) and the %dth (%.2f) is %.2f, if multiplied by %.4f then adds to %.4f." %(number_ind, number, residue, impulseresp[residue], number*impulseresp[residue], probability_waiting, probability_superposition))
			impulseresp_superposition.append(probability_superposition)
			print ("The final probability by superposition is %s." %str(impulseresp_superposition))
	return impulseresp_superposition




if "__main__" == __name__:
	print ("\n")
	C_List1 = ['ClkBuf', 'Counter', 'Load', 'SerDesCell']
	M_List1 = ['SPICE', 'Verilog']
	Sense_Dict1 = {'SPICE': [0.69, 0.76, 0.73, 0.18], 'Verilog': [0.68, 0.75, 0.72, 0.16]}
	# Block_Sensitivity_Draw(C_List1, M_List1, Sense_Dict1)
	C_List1 = ['ClkBuf', 'Counter', 'Load', 'SerDesCell']
	M_List1 = ['SPICE', 'Verilog']
	Pers_Dict1 = {'SPICE': [18, 221, 25, 23], 'Verilog': [12, 200, 20, 18]}
	# Error_Persistency_Draw(C_List1, M_List1, Pers_Dict1)

	# Nude Big
	C_List2 = ['ClkBuf', 'Counter', 'Load', 'SerDesCell']
	O_List2 = ['Clk', 'Cnt_Bit0', 'Cnt_Bit1', 'Cnt_Bit2', 'Load', 'SerDesOut']
	Sense_Dict2 = {'Clk': [0.88, 0, 0, 0], 'Cnt_Bit0': [0.29, 0.72, 0, 0], 'Cnt_Bit1': [0.28, 0.70, 0, 0], 'Cnt_Bit2': [0.30, 0.75, 0, 0], 'Load': [0.25, 0.75, 0.82, 0], 'SerDesOut': [0.16, 0.65, 0.71, 0.20]}
	# Block_Sensitivity_Draw(C_List2, O_List2, Sense_Dict2)
	C_List2 = ['ClkBuf', 'Counter', 'Load', 'SerDesCell']
	M_List2 = ['Mean', 'Max']
	Pers_Dict2 = {'Mean': [0.9, 25, 5, 5], 'Max': [12, 200, 20, 18]}
	# Error_Persistency_Draw(C_List2, M_List2, Pers_Dict2)

	# Nude Small
	C_List2 = ['ClkBuf', 'Counter', 'Load', 'SerDesCell']
	O_List2 = ['Clk', 'Cnt_Bit0', 'Cnt_Bit1', 'Cnt_Bit2', 'Load', 'SerDesOut']
	Sense_Dict2 = {'Clk': [0.82, 0, 0, 0], 'Cnt_Bit0': [0.25, 0.70, 0, 0], 'Cnt_Bit1': [0.24, 0.68, 0, 0], 'Cnt_Bit2': [0.26, 0.73, 0, 0], 'Load': [0.21, 0.70, 0.78, 0], 'SerDesOut': [0.11, 0.62, 0.68, 0.16]}
	# Block_Sensitivity_Draw(C_List2, O_List2, Sense_Dict2)
	C_List2 = ['ClkBuf', 'Counter', 'Load', 'SerDesCell']
	M_List2 = ['Mean', 'Max']
	Pers_Dict2 = {'Mean': [0.5, 15, 4, 4], 'Max': [12, 200, 20, 18]}
	# Error_Persistency_Draw(C_List2, M_List2, Pers_Dict2)

	# Reset
	C_List3 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesCell']
	O_List3 = ['Clk', 'Cnt_Bit0', 'Cnt_Bit1', 'Cnt_Bit2', 'Load', 'SerDesOut']
	Sense_Dict3 = {'Clk': [0.82, 0, 0, 0, 0], 'Cnt_Bit0': [0.25, 0.66, 0, 0.09, 0], 'Cnt_Bit1': [0.24, 0.64, 0, 0.08, 0], 'Cnt_Bit2': [0.26, 0.69, 0, 0.11, 0], 'Load': [0.21, 0.62, 0.78, 0.06, 0], 'SerDesOut': [0.11, 0.58, 0.68, 0.05, 0.16]}
	# Block_Sensitivity_Draw(C_List3, O_List3, Sense_Dict3)
	C_List3 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesCell']
	M_List3 = ['Mean', 'Max']
	Pers_Dict3 = {'Mean': [0.5, 3.2, 3.6, 3.8, 2.4], 'Max': [12.2, 19.2, 19.8, 19.2, 18.8]}
	# Error_Persistency_Draw(C_List3, M_List3, Pers_Dict3)

	# Resets
	C_List4 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesCell']
	O_List4 = ['Clk', 'Cnt_Bit0', 'Cnt_Bit1', 'Cnt_Bit2', 'Load', 'SerDesOut']
	#Sense_Dict4 = {'Clk': [0.82, 0, 0, 0, 0], 'Cnt_Bit0': [0.25, 0, 0, 0, 0], 'Cnt_Bit1': [0.24, 0, 0, 0, 0], 'Cnt_Bit2': [0.26, 0, 0, 0, 0], 'Load': [0.21, 0, 0, 0, 0], 'SerDesOut': [0.11, 0, 0.06, 0, 0.16]}
	# Block_Sensitivity_Draw(C_List4, O_List4, Sense_Dict4)
	C_List4 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesCell']
	M_List4 = ['Mean', 'Max']
	#Pers_Dict4 = {'Mean': [0.5, 0, 0.2, 0, 2.4], 'Max': [12.2, 0, 18.2, 0, 18.8]}
	# Error_Persistency_Draw(C_List4, M_List4, Pers_Dict4)

	# Full
	C_List5 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesCell']
	O_List5 = ['Clk', 'Cnt_Bit0', 'Cnt_Bit1', 'Cnt_Bit2', 'Load', 'SerDesOut']
	Sense_Dict5 = {'Clk': [0.82, 0, 0, 0, 0], 'Cnt_Bit0': [0.05, 0, 0, 0, 0], 'Cnt_Bit1': [0.04, 0, 0, 0, 0], 'Cnt_Bit2': [0.06, 0, 0, 0, 0], 'Load': [0.11, 0, 0, 0, 0], 'SerDesOut': [0.05, 0, 0, 0, 0]}
	# Block_Sensitivity_Draw(C_List5, O_List5, Sense_Dict5)
	C_List5 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesCell']
	M_List5 = ['Mean', 'Max']
	Pers_Dict5 = {'Mean': [0.4, 0, 0, 0, 0], 'Max': [2, 0, 0, 0, 0]}
	# Error_Persistency_Draw(C_List5, M_List5, Pers_Dict5)

	# Weird
	C_List6 = ['Raw', 'TMR1', 'TMR2', 'TMR3']
	O_List6 = ['Dose1', 'Dose2', 'Dose3']
	Sense_Dict6 = {'Dose1': [0.77, 0.28, 0.20, 0.15], 'Dose2': [0.66, 0.22, 0.16, 0.11], 'Dose3': [0.55, 0.18, 0.10, 0.05]}
	# Group_Bar_Draw(C_List6, O_List6, Sense_Dict6)
	C_List6 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesCell']
	M_List6 = ['Mean', 'Max']
	Pers_Dict6 = {'Mean': [0.4, 0, 0, 0, 0], 'Max': [2, 0, 0, 0, 0]}
	# Group_Bar_Draw(C_List6, M_List6, Pers_Dict6)

	### ===

	Strikes_List1 = ["LET=2", "LET=10", "LET=5", "LET=20"]
	Cell_List1 = ['ClkBuf', 'Counter', 'Load', 'SerDesOut']
	Distr_1 = [5, 12, 8, 15]
	Distr_2 = [24, 71, 52, 144]
	Distr_3 = [25, 65, 54, 122]
	Distr_4 = [36, 234, 72, 352]
	### Errors_Distributions_Draw(Strikes_List1, Cell_List1, Distr_1, Distr_2, Distr_3, Distr_4)

	Strikes_List2 = ["Nude", "Reset", "Half", "Full"]
	Cell_List2 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesOut']
	Distr_1 = [36, 234, 72, 0, 352]
	Distr_2 = [34, 188, 64, 54, 282]
	Distr_3 = [38, 42, 27, 24, 95]
	Distr_4 = [30, 37, 28, 29, 45]
	### Errors_Distributions_Draw(Strikes_List2, Cell_List2, Distr_1, Distr_2, Distr_3, Distr_4)

	# Strikes_List3 = ["Nude", "SDMR only", "SDMR+STMR", "TTMR+STMR", "STMR only"]
	Strikes_List3 = ["Nude", "TDMR", "SDMR", "TTMR", "STMR"]
	Cell_List3 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesOut']
	Distr_1 = [36, 234, 72, 0, 352]
	Distr_2 = [36, 50, 45, 38, 104]
	Distr_3 = [34, 40, 30, 33, 96]
	Distr_4 = [38, 38, 26, 26, 64]
	Distr_5 = [30, 37, 28, 29, 45]
	### Errors_Distributions_Draw(Strikes_List3, Cell_List3, Distr_1, Distr_2, Distr_3, Distr_4, Distr_5)

	Strikes_List4 = ["(50, 50, 10)", "(50, 50, 20)", "(100, 100, 10)"]
	Cell_List4 = ['ClkBuf', 'Counter', 'Load', 'Reset', 'SerDesOut']
	Distr_1 = [20, 48, 21, 22, 76]
	Distr_2 = [30, 63, 33, 29, 102]
	Distr_3 = [28, 45, 23, 24, 62]
	### Errors_Distributions_Draw(Strikes_List4, Cell_List4, Distr_1, Distr_2, Distr_3)

	### ===

	X_List1 = ['10ns', '5ns', '2ns']
	Y_List1 = ['Nude', 'Reset', 'LowTMR', 'HighTMR']
	Z_Dict1 = {'Nude': [224, 352, 541], 'Reset': [24, 50, 85], 'LowTMR': [12, 22, 36], 'HighTMR': [77, 128, 256]}
	X_List1 = ['10ns', '5ns', '2ns']
	Y_List1 = ['Nude(144)', 'Reset(162)', 'LowTMR(198)', 'HighTMR(442)']
	Z_Dict1 = {'Nude(144)': [224, 352, 541], 'Reset(162)': [24, 50, 85], 'LowTMR(198)': [12, 22, 36], 'HighTMR(442)': [77, 128, 256]}

	# Stuff_Bar_Draw(C_List3, M_List3, Pers_Dict3)
	# Stuff_Bar_Draw(X_List1, Y_List1, Z_Dict1)
	dict1 = {"a":"112", "b":"113", "c":"114", "d":"38", "e":"200", "f":"207"}
	dict2 = {"a":"1"}
	dict3 = {"treefruit":"apple", "stemfruit":"banana", "scrawlfruit":"grape", "treefruit":"orange", "d8":"diaos", "w":"wine"}
	dict4 = {"Array1":[1, 1, 5, 16, 35, 56, 80, 90, 95, 100], "Array2":[1, 1, 5, 20, 40, 78, 90, 92, 98, 100]}
	# print "\nThis is just a sorting test:", sorted(dict1.items(), key=lambda x: x[0]) # The dictionary is sorted by its keys.
	# print "\nThis is just a sorting test:", sorted(dict3.items(), key=lambda x: int(x[1])) # The dictionary is sorted by its values.

	list1 = [1, 2, 4, 8, 16]
	list1[0], list1[4] = list1[4], list1[0]
	print ("\nThis is just a list test:", list1)
	tuple1 = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
	dict5 = collections.defaultdict(list)
	for key, value in tuple1:
	    dict5[key].append(value)
	dict6 = {}
	for key, value in tuple1:
	    dict6.setdefault(key, []).append(value)
	print ("\nThis is just a dict test:", dict5.items())
	print ("\nThis is just a dict test:", dict6.items())
	print ("\n")

	test = '''
	step_list = [1, 2, 3, 4, 5]
	prob_list = [1, 4, 9, 16, 25]
	t = np.arange(0.0, 5.0, 0.02)
	mplplt.figure(figsize=(8,7), dpi=98)
	p1 = mplplt.subplot(211)
	p2 = mplplt.subplot(212)
	# p1.plot(step_list, prob_list)
	# p2.plot(step_list, prob_list)
	p1.plot(t,f1(t),"g-",label="$f(t)=e^{-t} \cdot \cos (2 \pi t)$")
	p2.plot(t,f2(t),"r-.",label="$g(t)=\sin (2 \pi t) \cos (3 \pi t)$", linewidth=2)
	p1.axis([0.0, 5.5, -1.0, 2.0])
	p1.set_ylabel("v", fontsize=14)
	p1.set_title("A decayed sine function", fontsize=18)
	p1.grid(True)
	p1.legend()
	p2.axis([0.0,5.01,-1.0,1.5])
	p2.set_ylabel("v", fontsize=14)
	p2.set_xlabel("t", fontsize=14)
	p2.legend()
	mplplt.show()
	'''

	cost_list1 = [82, 85, 94, 116, 134, 158]
	effectiveness_list1 = [0.66, 0.3, 0.1, 0.025, 0.011, 0.0098] # [0.642, 0.312, 0.1, 0.03, 0.02, 0.016] # [321, 156, 50, 15, 10, 8]
	# Optimization_Trace_Draw(cost_list1, effectiveness_list1)
	cost_list2 = [365, 377, 415, 484, 521, 586, 618, 666, 737, 777, 818, 855, 890] # [365, 415, 521, 618, 737, 858, 999]
	effectiveness_list2 = [0.88, 0.64, 0.45, 0.42, 0.32, 0.3, 0.28, 0.22, 0.12, 0.08, 0.045, 0.042, 0.04] # [0.88, 0.52, 0.42, 0.25, 0.12, 0.05, 0.04]
	# Optimization_Trace_Draw(cost_list2, effectiveness_list2)
	cost_list3 = [618, 653, 711, 771, 863, 917, 999, 1089, 1155, 1234] # [618, 711, 771, 917, 1089, 1234, 1555]
	effectiveness_list3 = [0.91, 0.6, 0.45, 0.3, 0.15, 0.1, 0.08, 0.05, 0.042, 0.04] # [0.91, 0.6, 0.3, 0.15, 0.08, 0.06, 0.05]
	# Optimization_Trace_Draw(cost_list3, effectiveness_list3)
	cost_list4 = [1001, 1050, 1111, 1199, 1234, 1331, 1444, 1525, 1666, 1789, 1900, 2020, 2111, 2222, 2345]
	effectiveness_list4 = [0.92, 0.78, 0.75, 0.62, 0.6, 0.58, 0.3, 0.25, 0.24, 0.18, 0.12, 0.08, 0.04, 0.03, 0.028]
	# Optimization_Trace_Draw(cost_list4, effectiveness_list4)
	cost_list5 = [1234, 1282, 1357, 1399, 1488, 1525, 1608, 1690, 1771, 1840, 1917, 2008, 2121, 2233, 2333, 2442, 2556, 2666]
	effectiveness_list5 = [0.93, 0.75, 0.72, 0.56, 0.55, 0.35, 0.3, 0.18, 0.17, 0.12, 0.11, 0.08, 0.05, 0.04, 0.03, 0.028, 0.026, 0.024]
	# Optimization_Trace_Draw(cost_list5, effectiveness_list5)
	cost_list6 = [2007, 2049, 2111, 2155, 2200, 2288, 2323, 2405, 2501, 2587, 2662, 2777, 2860, 2992, 3111, 3232, 3333, 3456, 3555, 3650, 3789, 3903, 4002, 4114, 4333, 4567, 4664]
	effectiveness_list6 = [0.94, 0.7, 0.5, 0.48, 0.47, 0.46, 0.36, 0.33, 0.3, 0.25, 0.24, 0.2, 0.18, 0.17, 0.15, 0.11, 0.09, 0.075, 0.068, 0.056, 0.055, 0.049, 0.047, 0.04, 0.033, 0.031, 0.0305]
	# Optimization_Trace_Draw(cost_list6, effectiveness_list6)

	cost_list10 = [82, 85, 94, 116, 134, 158]
	effectiveness_list10 = [2.5e-2, 1.5e-4, 1.5e-6, 2.75e-7, 2.25e-7, 2.05e-7]
	# Optimization_Trace_Draw(cost_list10, effectiveness_list10)
	cost_list11 = [82, 85, 94, 116, 134, 158]
	effectiveness_list11 = [9.5e-3, 5.5e-5, 3.9e-7, 2.5e-7, 2e-7, 1.75e-7]
	# Optimization_Trace_Draw(cost_list11, effectiveness_list11)
	cost_list12 = [365, 377, 415, 484, 521, 586, 618, 666, 737, 777, 818, 855, 890]
	effectiveness_list12 = [2.8e-3, 6.4e-4, 9.6e-5, 5.8e-5, 1.2e-5, 3.9e-6, 1.1e-6, 9.6e-7, 7.2e-7, 5.8e-7, 3.2e-7, 2.2e-7, 2e-7]
	# Optimization_Trace_Draw(cost_list12, effectiveness_list12)
	cost_list13 = [618, 653, 711, 771, 863, 917, 999, 1089, 1155, 1234]
	effectiveness_list13 = [6.4e-3, 6e-4, 8.8e-5, 1.2e-5, 6.8e-6, 3e-6, 9e-7, 5e-7, 4e-7, 3.6e-7]
	# Optimization_Trace_Draw(cost_list13, effectiveness_list13)
	cost_list14 = [1001, 1050, 1111, 1199, 1234, 1331, 1444, 1525, 1666, 1789, 1900, 2020, 2111, 2222, 2345]
	effectiveness_list14 = [3.2e-2, 7.8e-4, 7.8e-5, 6.2e-5, 6e-5, 5.8e-6, 4.6e-6, 1.4e-6, 9.4e-7, 8.8e-7, 7.2e-7, 5.8e-7, 4e-7, 3.9e-7, 3.8e-7]
	# Optimization_Trace_Draw(cost_list14, effectiveness_list14)
	cost_list15 = [1234, 1282, 1357, 1399, 1488, 1525, 1608, 1690, 1771, 1840, 1917, 2008, 2121, 2233, 2333, 2442, 2556, 2666]
	effectiveness_list15 = [9.5e-2, 8.5e-4, 2.2e-4, 5.7e-5, 1.5e-5, 8.5e-6, 7.3e-6, 5.9e-6, 3.7e-6, 1.1e-6, 9.1e-7, 7.7e-7, 5.5e-7, 4.3e-7, 3.1e-7, 2.7e-7, 2.6e-7, 2.5e-7]
	# Optimization_Trace_Draw(cost_list15, effectiveness_list15)
	cost_list16 = [2007, 2049, 2111, 2155, 2200, 2288, 2323, 2405, 2501, 2587, 2662, 2777, 2860, 2992, 3111, 3232, 3333, 3456, 3555, 3650, 3789, 3903, 4002, 4114, 4333, 4567, 4664]
	effectiveness_list16 = [9.6e-2, 8.7e-3, 7.5e-4, 6.1e-4, 2.7e-4, 1.1e-4, 3.3e-5, 2.3e-5, 1.9e-5, 8.5e-6, 8.1e-6, 7.5e-6, 7.1e-6, 3.7e-6, 2.1e-6, 1.9e-6, 1.3e-6, 1e-6, 8.9e-7, 8.3e-7, 7.5e-7, 6.9e-7, 5.7e-7, 5.4e-7, 5.3e-7, 5.1e-7, 5e-7]
	# Optimization_Trace_Draw(cost_list16, effectiveness_list16)


	cost_list20 = [82, 94, 85, 116, 134, 158]
	effectiveness_list20a = [2.5e-2, 1.5e-4, 1.5e-6, 2.75e-7, 1.25e-7, 6.5e-8] # [2.5e-2, 1.5e-4, 1.5e-6, 2.75e-7, 2.25e-7, 2.05e-7]
	effectiveness_list20b = [9.5e-4, 1.1e-5, 5.9e-7, 2e-7, 1e-7, 6e-8] # [9.5e-3, 5.5e-5, 3.9e-7, 2.5e-7, 2e-7, 1.75e-7]
	effectiveness_list20c = [1.1e-4, 3.5e-6, 3.5e-7, 1.5e-7, 8e-8, 5e-8]
	effectiveness_list20d = [2.5e-5, 1.3e-6, 2.3e-7, 1.1e-7, 7e-8, 4e-8]
	Optimization_Traces_Draw(cost_list20, effectiveness_list20a, effectiveness_list20b, effectiveness_list20c, effectiveness_list20d)

	cost_list21 = [82, 85, 94, 116, 134, 158]
	effectiveness_list21a = [2.5e-2, 1.5e-4, 1.5e-6, 2.75e-7, 1.25e-7, 6.5e-8] # [2.5e-2, 1.5e-4, 1.5e-6, 2.75e-7, 2.25e-7, 2.05e-7]
	effectiveness_list21b = [9.5e-4, 1.1e-5, 5.9e-7, 2e-7, 1e-7, 6e-8] # [9.5e-3, 5.5e-5, 3.9e-7, 2.5e-7, 2e-7, 1.75e-7]
	effectiveness_list21c = [1.1e-4, 3.5e-6, 3.5e-7, 1.5e-7, 8e-8, 5e-8]
	effectiveness_list21d = [2.5e-5, 1.1e-6, 2.3e-7, 9e-8, 7e-8, 4e-8]
	Optimization_Traces_Draw(cost_list21, effectiveness_list21a, effectiveness_list21b, effectiveness_list21c, effectiveness_list21d)

	cost_list22 = [365, 373, 385, 399, 422, 484, 520, 544, 618, 666, 737, 777, 818, 898]
	effectiveness_list22a = [2.8e-3, 6.4e-4, 9.6e-5, 5.8e-5, 1.1e-5, 3.9e-6, 7.2e-7, 1.2e-7, 7.8e-8, 2.2e-8, 7.6e-9, 3.8e-9, 1.2e-9, 9.2e-10]
	effectiveness_list22b = [5.6e-5, 5.2e-6, 9.2e-7, 6.5e-7, 9.8e-8, 3.9e-8, 1.1e-8, 7.8e-9, 6.2e-9, 3.8e-9, 1.8e-9, 1.4e-9, 8.2e-10, 6.8e-10]
	effectiveness_list22c = [2.2e-6, 2.4e-7, 7.6e-8, 5.8e-8, 2.2e-8, 9.9e-9, 3.1e-9, 2.1e-9, 1.7e-9, 1.3e-9, 9.6e-10, 7.8e-10, 6.2e-10, 5.2e-10]
	effectiveness_list22d = [1.8e-7, 2.2e-8, 9.8e-9, 9.2e-9, 5.8e-9, 3.2e-9, 1.2e-9, 1e-9, 9.2e-10, 8.8e-10, 7.2e-10, 6.6e-10, 5.2e-10, 4.8e-10]
	Optimization_Traces_Draw(cost_list22, effectiveness_list22a, effectiveness_list22b, effectiveness_list22c, effectiveness_list22d)

	cost_list23 = [618, 626, 653, 688, 711, 771, 863, 917, 999, 1089, 1155, 1234, 1299, 1333, 1399, 1441, 1501]
	effectiveness_list23a = [6.4e-3, 6e-4, 8.8e-5, 1.2e-5, 6.8e-6, 2e-6, 6.8e-7, 2.4e-7, 7.8e-8, 3.8e-8, 1.2e-8, 7.2e-9, 3.2e-9, 1.8e-9, 1.2e-9, 9.4e-10, 8.4e-10]
	effectiveness_list23b = [2.4e-5, 4e-6, 7.8e-7, 2.6e-7, 9.8e-8, 5e-8, 2.8e-8, 1.4e-8, 9.4e-9, 7.8e-9, 3.8e-9, 2.8e-9, 1.2e-9, 9.6e-10, 8.2e-10, 7.2e-10, 6.8e-10]
	Optimization_Traces_Draw(cost_list23, effectiveness_list23a, effectiveness_list23b)

	cost_list24 = [1001, 1019, 1049, 1088, 1111, 1199, 1234, 1278, 1331, 1389, 1422, 1488, 1555, 1608, 1688, 1789, 1840, 1921, 2020, 2111, 2222, 2345]
	effectiveness_list24a = [1.2e-1, 9.8e-3, 1.8e-3, 9.2e-5, 5e-5, 9.8e-6, 7.6e-6, 5.4e-6, 9.4e-7, 6.8e-7, 3.2e-7, 1.6e-7, 7.4e-8, 1.6e-8, 9.2e-9, 6.8e-9, 3.4e-9, 9.6e-10, 5.8e-10, 3.2e-10, 1.8e-10, 9.8e-11]
	effectiveness_list24b = [1.2e-3, 1.2e-4, 3.2e-5, 2.2e-6, 1e-6, 4.8e-7, 3.6e-7, 2.2e-7, 8.4e-8, 6.2e-8, 4.2e-8, 2.6e-8, 8.6e-9, 4.4e-9, 2.2e-9, 1.4e-9, 5.2e-10, 3.8e-10, 2.2e-10, 1.6e-10, 9.2e-11, 7.4e-11]
	Optimization_Traces_Draw(cost_list24, effectiveness_list24a, effectiveness_list24b)
	cost_list25 = [1234, 1256, 1282, 1331, 1355, 1399, 1444, 1488, 1525, 1575, 1618, 1690, 1733, 1777, 1840, 1917, 1983, 2017, 2050, 2121, 2233, 2333, 2442, 2500, 2600, 2699]
	effectiveness_list25a = [1.5e-1, 1.8e-2, 2e-3, 4e-4, 9.5e-5, 7.7e-5, 3.5e-5, 8.3e-6, 4.5e-6, 1.9e-6, 7.9e-7, 5.5e-7, 1e-7, 8.5e-8, 5.5e-8, 2.1e-8, 9.9e-9, 7.1e-9, 6.3e-9, 3.3e-9, 1.1e-9, 9.5e-10, 5.8e-10, 3.2e-10, 1.8e-10, 1.2e-10]
	effectiveness_list25b = [7.5e-4, 8.8e-5, 2e-5, 5e-6, 1.5e-6, 1.1e-6, 7.5e-7, 3.5e-7, 1.5e-7, 8.9e-8, 6.9e-8, 5.5e-8, 2e-8, 9.9e-9, 7.5e-9, 5.1e-9, 3.1e-9, 1.9e-9, 1.3e-9, 9.7e-10, 4.1e-10, 3.5e-10, 2.3e-10, 1.7e-10, 1.1e-10, 9.2e-11]
	Optimization_Traces_Draw(cost_list25, effectiveness_list25a, effectiveness_list25b)

	X_List1 = ['0.5', '0.25', '0.1', '0.05'] # ['High', 'Medium High', 'Medium Low', 'Low']
	Y_List1 = ['Nude', 'Sol0', 'Sol1', 'Sol2', 'Sol3']
	# Z_Dict0 = {'Nude':[485, 321, 180, 128], 'Sol0':[188, 108, 24, 8], 'Sol1':[60, 32, 20, 5], 'Sol2':[30, 15, 10, 3], 'Sol3':[16, 10, 8, 3]}
	Z_Dict1 = {'Nude':[0.97, 0.642, 0.36, 0.256], 'Sol0':[0.375, 0.216, 0.048, 0.016], 'Sol1':[0.12, 0.064, 0.025, 0.01], 'Sol2':[0.06, 0.03, 0.02, 0.006], 'Sol3':[0.032, 0.02, 0.016, 0.006]}
	# Group_Bar_Draw(X_List1, Y_List1, Z_Dict1)
	X_List2 = ['1M', '100K', '10K', '1K']
	Y_List2 = ['Nude', 'Sol0', 'Sol1', 'Sol2', 'Sol3']
	Z_Dict2 = {'Nude':[2.5e-2, 9.5e-3, 1.5e-3, 5.5e-4], 'Sol0':[1.5e-4, 1.25e-5, 7.5e-7, 1.75e-7], 'Sol1':[1.5e-6, 7.5e-7, 1.75e-7, 1.35e-7], 'Sol2':[2.75e-7, 2.5e-7, 1.55e-7, 1.25e-7], 'Sol3':[2.25e-7, 2e-7, 1.5e-7, 1.25e-7]}
	# Group_Bar_Draw(X_List2, Y_List2, Z_Dict2)

	list1 = [0.6, 0.5, 0.4, 0.0]
	list2 = [0.0, 0.5, 0.1, 0.0]
	list3 = [0.1, 0.0]
	list4 = []
	list12 = []
	list123 = [[0.6, 0.5, 0.4, 0.0], [0.5, 0.1, 0.0, 0.0], [1]]
	# convl = np.convolve(np.convolve(list1, list2), list3)
	# convl = reduce(np.convolve, list123)
	# list12 = reduce(lambda x, y: x.append(y), sum(item for item in zip(list1, list2)))

	for item in zip(list1, list2):
		print ("Before zipping", item, sum(item))
		list12.append(sum(item))
	for item in zip(*list123):
		list4.append(sum(item)/len(item))
		print ("After zipping", item, list4)
	list4 = [iter(list3)] * 5
	zipper = zip_longest(*list123, fillvalue=0)
	# print ("The convolution is:", convl)
	print ("The duplication is:", list4, random.choice(list4))
	Func_Star(*list1)
	Func_Star(**dict4)

	# print "\nThe sorting is:\n", sorted(set(list2), key=list2.index) # [0.0, 0.5, 0.10000000000000001]
	print ("\nThe residue is:\n", Func_Voting([0, 0, 0.25, 0, 0.06, 0, 0.02, 0], 5, 2))
	# print "\nThe probability is:", Func_Probability(4, 0.1, 2)
	# print "\nThe probability is:", Func_Probability(10, 0.1, 2)

# END


s='''

Analysis of Soft Error Mitigation Effects as a Function of Dose Rate and LET

Goal:
Evaluation of the probability of system-level failure expressed in the frequency and strength of soft errors.

Assumptions:
Device-level behavior and probalitities modeled by existing work.
Propagation of errors away from the initial strike is conventional logic modeling.

Observation:
Long-duration, widely-spread, or high-LET errors escape from mitigation.
Seemingly equivalent soft error coverage solutions exhibit radically different measured error rates.
Alternative mitigation strategies have enormous different implementation costs.

Thesis:
Evaluation of mitigation techniques in high radiation environments must consider error propagation and duration.
Error propagation describes the number of nodes affected by a single event error.
Error duration is the total time between error injection and mitigation.

Hierarchical mitigation offers a flexible approach to trade-off mitigation effectness and design costs.

Physical process behind soft errors

Soft error generation
Soft error what is it
Soft error propagation
Soft error and flip flops, duration changed. Conventionally every ff is treated as crutial. The only importance of ff is the modification of duration. 

Essentially mitig affect duration, propagation, and cross-s vs let.

'''
