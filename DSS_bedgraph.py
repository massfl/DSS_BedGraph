import pandas as pd
import gzip
import shutil
import os

def DSS_bedgraph(DSS_output_file_and_path,
	output_file_and_path,
	Cytosine_context,
	mu1 = "Control",
	mu2 = "Experimental",
	RGB_track_color = [(102, 204, 255), (51, 204, 51)],
	per_chr = True,
	full_bedGraph = True):
	
	#a functtion to convert DSS output files into BedGraphs with the possibility to adjust in file description and final tracks color
	#mu1 and 2 are the mean methylation values for the two samples that are being compared in the DSS analysis
	#DSS_bedgraph() will draw a bedgraph file for each sample so mu1 and 2 need to be asigned a sample name
	#cytosine context is a string indicating the type of cytosine (CpG, CpH etc..)

	#Open a file to write the data in and write some coment lines at the begining of the file, it will tell the file type, name of the samples and color of the visulaized track
	def save_and_name_BedGraph(chr_meth_data_input,
		output_file_and_path,
		chr_name,
		sample,
		Cytosine_context,
		RGB_track_color = (102, 204, 255)):


		#define the path and name of the saved file
		file_name = "{}{}_{}_{}.bedGraph".format(output_file_and_path, sample, Cytosine_context, chr_name)
		compressed_file_name = "{}{}_{}_{}.bedGraph.gz".format(output_file_and_path, sample, Cytosine_context, chr_name)

		#create a file object in the append mode
		file = open(file_name, "a")
		#Append a bedgraph header line in the fileobject
		file.write("track type=bedGraph name={} color={},{},{}\n".format(chr_name+sample+Cytosine_context, RGB_track_color[0], RGB_track_color[1], RGB_track_color[2]))
		#append the content of the to_csv() method result
		chr_meth_data_input.to_csv(file, header = False, index = False, sep ="\t", compression = "gzip")
		#close the file
		file.close()
		
		#reopen the file in a read binary mode this time
		binary_bedGraph = open(file_name, "rb")
		#create a gzip compressed file object in the write binary mode
		compressed_file_obj = gzip.open(compressed_file_name, "wb")
		#copy the content of the binary file into the compressed binary file
		shutil.copyfileobj(binary_bedGraph, compressed_file_obj)

		#close the files
		binary_bedGraph.close()
		compressed_file_obj.close()

		#remove the non Compressed bedGraph file
		os.remove(file_name)


	#open the DSS output file
	cyto = pd.read_csv(DSS_output_file_and_path, sep = "\t", usecols = ["chr", "pos", "mu1", "mu2"], compression = "gzip")
	cyto.convert_objects(convert_numeric=True)




	Methylation_sample_names_and_color = [("mu1", mu1, RGB_track_color[0]), ("mu2", mu2, RGB_track_color[1])]
	
	for mean_meth, sample_name, track_color in Methylation_sample_names_and_color:

		#the following piece of code creates the actual bedGraph files
		#Note a UCSC bedgraph is 0 based |N|C|G|N|
		#                    		 / /  \ \
		#                   		0 1   2  3

		cytoBed = pd.DataFrame()
		cytoBed["chr"] = cyto.loc[:, "chr"]
		cytoBed["start"] = cyto.loc[:, "pos"] -1
		cytoBed["end"] = cyto.loc[:, "pos"]
		cytoBed["mean_meth"] =cyto.loc[:, mean_meth]



		if per_chr:

			#the data is divided by chromosome to make many smaller chromosome specific bedGraphs
			groupbed = cytoBed.groupby(by="chr")

			for group_name, group_values in groupbed:

				save_and_name_BedGraph(chr_meth_data_input = group_values,
					sample = sample_name,
					chr_name = group_name,
					Cytosine_context = Cytosine_context,
					output_file_and_path = output_file_and_path,
					RGB_track_color = track_color)
	
		else:
			pass



		if full_bedGraph:

			save_and_name_BedGraph(chr_meth_data_input = cytoBed,
				sample = sample_name,
				chr_name = "AllChr",
				Cytosine_context = Cytosine_context,
				output_file_and_path = output_file_and_path,
				RGB_track_color = track_color)

		else:
			pass

	
