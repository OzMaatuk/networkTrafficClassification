## Neural Network Classification - Not Completed.

# adapted from Simons Project.

this project using the Keras 2D Convolution Neuron Network model, to classify the BOA of network traffic samples.
this approach using samples as a size-time histogram of packets (each sample indicates network session).
the samples are pickle files that represent the size-time histogram of network session (pcap file).


pcaptohistpkl.py, pcaptopkl.py - creates a pickle file of packets size timely ordered to represent a size-time histogram.


anlzpkl.py, anlzhistpkl.py - creates a gif picture of the histogram graph from a proper pickle file.


pcaptopic.py - takes all pickles in the "pickles" folder and created a matched gif picture of histogram graphs (samples) in pics. using the previous scripts.


Nets32.ipynb - NN model code from Saimons Project (training and test-training).


nets32.py - the adapted NN model code for this project, in progress.


the model architecture based on ...
