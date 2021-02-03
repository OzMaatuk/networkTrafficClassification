## Datasets.

the datasets that motivated this project was collected at the Ariel University Cyber Lab to serve several learning projects.
it built by creating .pcap samples (Wireshark file for recording network traffic) of known use.
those .pcap files have a label by the tuple < Browser, Operation-System, Application > which refers to BOA.
with about 20GB of .pcap samples, a properly featured dataset was extracted as a CSV file,
in honor of Jonathan features-extraction project: https://github.com/JonMuehlst/pcap-feature-extractor

any column in the CSV file refers to specific features.
and any row refers to a recorded session (pcap file).
the feature list can be found here: https://drive.google.com/file/d/1F-mhaZnhDijgoogQLQJR54vXzcGj5i4b/view?usp=sharing


samples_25.2.16_all_features_triple.csv - is the original dataset file adapted from Jonathan Research.


tuple_dataset - is the main form of dataset been used.
includes several forms of the original dataset, with modification.
(adding labels, converting values, and optimizing features set)


os_dataset, browser_dataset, app_dataset - been created to make an individual classification.
same as tuple_dataset when the label used in operation-system/browser/application and not the whole tuple


DB_scripts - python scripts have been used to manage the dataset.
an operation like setting the labels to proper text in each column title,
splitting the data to train and test randomly, and creates answers file, for evaluation.
"all_features_tuple_train" is a random split of the "all_features_tuple" dataset with 70% of the data.
the data set CSV format separate columns by TAB ('\t'), and the [1] line is the columns index line.


NOTE: like all other values, the BOA label of each sample is numeric, and presenting the OS with the last digit, Browser with two digits in the middle, and Application with the first two digits. so the label is 5 digits number.