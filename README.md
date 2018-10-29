# DSS_BedGraph

A python3 module to transform DSS output methylation files into UCSC browser compatible BedGraph files that contain methylation levels (0 to 1) at individual cytosines

This module is primarily composed of the DSS_bedgraph() function. It takes DSS output methylation files as input. 
a DSS methylation file contains information about methylation levels at individual cytosines for two experimental conditions ("mu1" and "mu2"). Each experimental condition is transformed into BedGraph format. 

Moreover,  DSS_BedGraph can generate whole genome or chromosomes-specific BedGraph files.

DSS_BedGraph is a python3 module that requires pandas


**USAGE**

DSS_bedgraph(DSS_output_file_and_path, output_file_and_path, Cytosine_context, mu1 = "Control", mu2 = "Experimental", RGB_track_color = [(102, 204, 255), (51, 204, 51)], per_chr = True, full_bedGraph = True):

**parameters:**                 

                             .DSS_output_file_and_path: full path to the DSS methylation file
                             
                             .output_file_and_path: full path to the folder where to save the BedGraph files
                             
                             .Cytosine_context: a string documenting the type of cytosine methylation that will be used to call the             
                              output file (e.g "CG" or "CH")    
                              
                             .mu1: a string indicating the name of sample 1, default: "Control"
                             
                             .mu2: a string indicating the name of sample 2, default: "Experimental"
                             
                             .RGB_track_color: a list of tuples containing RGB color values for each samples, default [(102, 204, 255), (51, 204, 51)] so that sample1 is blue and sample is green
                             
                             .per_chr: boolean, if True will generate a separate BedGraph file for each chromosome, default: True
                             
                             .full_bedGraph: boolean, if True will generate a whole genome BedGraph file, default: True
                             
                           
**EXAMPLE**

DSS_bedgraph(DSS_output_file_and_path = "/Users/username/methyl_CpG_DSS_test.txt.gz", output_file_and_path = "/Users/username/", mu1 = "sample1", mu2 = "sample2", RGB_track_color = [(102, 204, 255), (51, 204, 51)], Cytosine_context = "CpH", per_chr = True, full_bedGraph = True)
                             
                                          
Result: a .BedGraph.gz file that can be uploaded onto the UCSC browser, see below:


![ucsc_track_test_dss_bedgraph](https://user-images.githubusercontent.com/36674021/47677514-b64e6080-db95-11e8-8f75-3e4f7af58ced.png)
                   
                              
                              
