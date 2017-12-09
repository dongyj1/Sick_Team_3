# -Learning From Sensor Data-


# 1. Project Task
Our project is to investigate the relationship between different attributes and learn some potential rules from the dataset provided by SICK. 
We are given 5 expectation questions which are:

•	Across the entire dataset, what can we learn about _package trends_ with respect to LFT (Legal For Trade) and NotLFT (not Legal For Trade) conditions.

•	How does the belt speed behave across time? Are there any correlations between belt speed and NotLFT (or LFT)?

•	Investigate “Gap” information and determine if there are any observable outliers. Correlate this information with the differences in the timestamps between adjacent packages

•	What can we learn about “Pileup” or “Log Jam” situations? Are trends in conditions such as Irreg, MultiRead, TooBig indicative of this phenomenon?

•	In general, identify outliers in the data: 

o	Random changes in the units – example: ft/min changes to m/sec

o	Total Throughput changes, Specific throughput based on conditions

o	Recurring errors observed in the Heart Beat data section

To sum up, We need to build a classification model which the output label is LFT and the input attributes are other condistions and information. We also need to figure out how to transfer package trends, 'Pileyp', 'Log Jam' to clear data.

# 2. Related Work
# 3. Approach
## 3.1 LFT Condition Exploration

We first implement Logistic Regression, SVM, random forest, Adaboost and MLP to predict the LFT label.
Out input array is 
We found out if we took condition ValidRead and ValidDim as input, we could predict LFT label with 100 percent. 

## 3.2 Speed Attribute Evaluation
For evaluating the belt speed over time, we firstly plot the time series to ituitively show the speed behavior. And then we also found the mean and deviation value in one single day and in the whole time. About the analysis of correlation between the belt speed and LFT/Not LFT label, we calculate the correlation on every single day and we also used LSTM to analyze the effect of belt speed on LFT. 
## 3.3 Gap Information 

## 3.4 "Pipe Up" & "Log Jap"

## 3.5 Outlier Detection

# 4. Dataset and Metric


# 5. Evaluation


# 6. Conclusion


# 7. Roles






