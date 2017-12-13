# How to run the code
## 1. environment requirment
python 3.6.2, keras 2.0.6, numpy, pandas, matplotlib, scikit-learn, tensorflow r1.4 cpu version are required

We recommend you use anaconda to install those packages, please run following commands in your anaconda prompt in Windows(terminal in macOS/Linux):
For scikit-learn:
> conda install -c anaconda scikit-learn

For pandas:
>conda install pandas

For keras:
>conda install -c conda-forge keras

For Tensorflow, run these commands respectively :
>conda create -n tensorflow python=3.6

>activate tensorflow

>pip install --ignore-installed --upgrade tensorflow 

## 2. How to run our code
1.For LFT Condition Prediction problem, first you can try several basic models: Logistic Regression, SVM, Random Forest, MLP. 
>python Classifiers.py


2.For LFT Condition Exploration problem with LSTM model, run:
>python LSTM_model.py

Before you run, you need to change "path" to the path direct to "proagain" folder in your computer.
Expected figure shown:
![alt text](https://github.com/dongyj1/Sick_Team_3/blob/master/images/f1_10days_10n_64b_10e_.png)
![alt text](https://github.com/dongyj1/Sick_Team_3/blob/master/images/loss_10days_10n_64b_10e_.png)
![alt text](https://github.com/dongyj1/Sick_Team_3/blob/master/images/pr_10days_10n_64b_10e_.png)
You can also get rating value such as loss and f1 score in the console.

3.For LFT Condition Exploration problem with LSTM model and time interval feature added, run:
(Before you run, you need to change "path" to the path direct to "proagain" folder in your computer.)
>python LSTM_modelF_withTimeInterval.py

Similar results should be shown.

2.For Gap Information problem run:
>python oga_analysis.py

3.For "Pile Up" & "Log Jam" problem run:
>python prob_4.py

4.For getting the belt speed change over time run:
>python speed_time_analysis.py

5.For getting the correlation between belt speed and LFT:
>python corelation_analysis.py


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

Since we need to evaluate the information behind the trend and build a classifier for LFT label, we first implemented some classic classification algorithms such as logistic regression, SVM, MLP and random forest via scikit-learn. Also, for adding time series information of packages (packages trend information), we consider our classification problem as a time series problem with multiple input variables which we found some experience [here](https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/). In the mean time, we also research some other algorithms for time series such as Hidden Markov Model in this [blog](https://codefying.com/2016/09/15/a-tutorial-on-hidden-markov-model-with-a-stock-price-example/) and LSTM in [Reducing the Dimensionality of Data with Neural Networks](http://science.sciencemag.org/content/313/5786/504). Apart from building the model, We also learn how to tune the LSTM hyperparameter in this [blog](https://machinelearningmastery.com/tune-lstm-hyperparameters-keras-time-series-forecasting/).

# 3. Approach
## 3.1 LFT Condition Exploration

We first implement Logistic Regression, SVM, random forest, Adaboost and MLP to predict the LFT label.
Out input array is 
We found out if we took condition ValidRead and ValidDim as input, we could predict LFT label with 100 percent. 

## 3.2 Speed Attribute Evaluation
For evaluating the belt speed over time, we firstly plot the time series to intuitively show the speed behavior. And then we also found the mean and deviation value in one single day and in the whole time. About the analysis of correlation between the belt speed and LFT/Not LFT label, we calculate the correlation on every single day and we also used LSTM to analyze the effect of belt speed on LFT. 
## 3.3 Gap Information 
  For outlier determination with gap information and timestamp, after plotting all the relevant data it is shown that the Gap condition is determined only by “oga” and objects with negative "oga" should be outliers.
   To get the boundary for Gap information specific, we implemented Logistic Regression and Robust linear model. 
   First, to get the relation between "oga" information and each adjacent objects' time interval, we use Robust linear model to fit the data. The input of Robust model is [x = array(time interval information) , y = array("oga")] and the output is co-efficiency of these two variables. The result intends that it is not necessary to consider both time interval and "oga" for "Gap" investigation.
   After plotting the "oga" and it's "Gap" condition, it is clearly separated into two parts along "oga" value. So we used SVM module to implement it. The input of SVM module is “oga” without negative data, which is split using cross_validation.train_test_split() function imported from Sklearn. The kernel of SVM is "linear" and it specifies the epsilon-tube within which no penalty is associated in the training loss function with points predicted within a distance epsilon from the actual value. The output of this model is the classification. We calculate the threshold from the module by "threshold = (-clf.intercept_/clf.coef_).flatten()[0]". For all the objects with "Gap" but not in the classification result, we call them detectived outliers.
## 3.4 "Pile Up" & "Log Jam"
Since there is no "Pile Up" & "Log Jam" label in the data, we need to identify "Pile Up" & "Log Jam" situation first. The gap between each package would be the main criteria to identify "Pile Up" & "Log Jam" situation. From gap information we know when gap is smaller than -1000, it is equal to "side by side" condition, so we would say all the packages whose gap is smaller than -1000 have "Pile Up" & "Log Jam" situation. Moreover, if "Gap" condition appears in package data, it means the gap distance between packages is smaller than 15 inches. So if "Gap" condition appears continuously, we would say those packages with "Gap" condition are in "Pile Up" & "Log Jam" situation.

the input of the model is all the “Irreg”, “MultiRead”, “TooBig” condition in the package data, the shape of the input is [1657178, 3], the output of the model is the predicted "pile up" condition, the shape of the input is [1657178, 1]. Since this is a classification problem, we use logistic regression and MLP and SVM with RBF kernel. 

In logistic regression and MLP, we use Relu as activation function and the loss function is:

![logistic_regression_loss](http://latex.codecogs.com/gif.latex?L%28%5Ctheta%29%20%3D%20-%5Cfrac%7B1%7D%7Bm%7D%5B%5Csum%5Em_%7Bi%20%3D%201%7Dy%5E%7B%28i%29%7Dlog%20h_%5Ctheta%28x%5E%7B%28i%29%7D%29%20&plus;%20%281-y%29%5E%7B%28i%29%7Dlog%20%281%20-%20h_%5Ctheta%28x%5E%7B%28i%29%7D%29%29%5D)

where: ![logistic_regression_hype](http://latex.codecogs.com/gif.latex?h_%5Ctheta%28x%29%20%3D%20log%281%20&plus;%20exp%28x%29%29) is the activation function,x is input and y is output.

Hyper-parameter:
For logistic regression ![lambda](http://latex.codecogs.com/gif.latex?%5Clambda) = 10,  L2 regularization
For MLP ![alpha](http://latex.codecogs.com/gif.latex?%5Calpha) = 0.0001, ![lambda](http://latex.codecogs.com/gif.latex?%5Clambda) = 10,  L2 regularization, hidden_layer_sizes = (20, 4)

In SVM with RBF kernel, the loss function is:

![SVM_loss](http://latex.codecogs.com/gif.latex?L%28%5Ctheta%29%20%3DC%5B%5Csum%5Em_%7Bi%20%3D%201%7Dy%5E%7B%28i%29%7Dcost_1%28%5Ctheta%5ETf%5E%7B%28i%29%7D%29%20&plus;%20%281-y%29%5E%7B%28i%29%7Dcost_0%28%5Ctheta%5ETf%5E%7B%28i%29%7D%29%5D%20&plus;%20%5Cfrac%7B1%7D%7B2%7D%5Csum%5En_%7Bj%20%3D%201%7D%5Ctheta%5E2_j)

where: ![SVM_gauss](http://latex.codecogs.com/gif.latex?f%5E%7Bi%7D%20%3D%20exp%28-%5Cfrac%7B%7C%7Cx-x%5E%7B%28i%29%7D%7C%7C%5E2%7D%7B2%5Csigma%5E2%7D%29) for gauss kernel, 

Hyper-parameter: C = 2, ![gamma_value](http://latex.codecogs.com/gif.latex?%5Cgamma%20%3D%20100) where ![gamma_sigma](http://latex.codecogs.com/gif.latex?%5Cgamma%20%3D%202%5Csigma%5E%7B-2%7D)

## 3.5 Outlier Detection
### 3.5.1 Unit outlier
There are not many unit outliers in the dataset. For all the units, only speed_unit, otl_unit, oga_unit, size_unit, obv_unit and orv_unit has randomly changed for 895 times. And furthermore, all these units changed at the same time for a object observation. They are all showing randomly in the data sets. Although the units are changed, the value changed correspondingly, so the final results won't be affected.

### 3.5.3 Recurring errors in the Heart Beat data
Recurring errors can be defined as same error occured on each device. In order to count the number of each device's error, we checked each heartbeat file and get the number of all relative data for 6 devices. As a result, device 5 had lowest error occur while others were similar.
  
# 4. Dataset and Metric
Our dataset is provided in XML format which includes two kinds of information object data and heartbeat data. Object data corresponds to information collected from every single package through the camera. Heartbeat data refers to the state of the sensor system. We extracted original data from XML files into several CSV files. In the XML file, each object and heartbeat is stored as an element tree. We implemented DFS algorithm to traverse each root’s children and extracted useful data into a dictionary. As a result, for each XML file, the valid data is stored in two CSV files, one is for object data and the other is for heartbeat data.

# 5. Evaluation

# 6. Conclusion
## 6.1 LFT Condition Exploration
## 6.2 Speed Attribute Evaluation
## 6.3 Gap detection
For outlier determination with Gap and correlative with timestamp, it is shown that the relation about oga(gap information) and time interval for each object is clearly linear. And the boundary of oga which is used to determine Gap condition is 15.12967427. It is caculated by the coef_ and intercept_ of SVM module.


