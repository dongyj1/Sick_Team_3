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
  For outlier determination with gap information and timestamp, after plotting all the relevant data it is shown that the Gap condition is determined only by “oga” and objects with negative "oga" should be outliers.
To get the boundary for Gap information specific, we implemented Logistic Regression and Robust linear model. 
First, to get the relation between "oga" information and each adjacent objects' time interval, we use Robust linear model to fit the data and the result detected few outliers, which means time interval bewteen two adjacent objects and "oga" information is linearly dependent. So it is not necessary to consider both time interval and "oga" for "Gap" investigation.
	After plotting the "oga" and it's "Gap" condition, it is clearly separated into two parts along "oga" value. So we used logistic regression to implement. The input of logistic regression is “oga” without negative “oga” objects, which is split using cross_validation.train_test_split() function imported from Sklearn. And the output of this model is the linear relation and the boundary of data.
## 3.4 "Pipe Up" & "Log Jap"

## 3.5 Outlier Detection

# 4. Dataset and Metric


# 5. Evaluation


# 6. Conclusion


# 7. Roles






