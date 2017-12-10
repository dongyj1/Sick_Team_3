# -Learning From Sensor Data-
SICK 3: Changlong Jiang, Yangjiang Dong, Gaomeizhu Qu, Yuxuan Su

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

## 3.2 Speed Attribute Evaluation

## 3.3 Gap Information 

## 3.4 "Pipe Up" & "Log Jap"
Since there is no "Pile Up" & "Log Jam" label in the data, we need to identify "Pile Up" & "Log Jam" situation first. The gap between each package would be the main criteria to identify "Pile Up" & "Log Jam" situation. From gap information we know when gap is smaller than -1000, it is equal to "side by side" condition, so we would say all the packages whose gap is smaller than -1000 have "Pile Up" & "Log Jam" situation. Moreover, if "Gap" condition appears in package data, it means the gap distance between packages is smaller than 15 inches. So if "Gap" condition appears continuously, we would say those packages with "Gap" condition are in "Pile Up" & "Log Jam" situation.

the input of the model is all the “Irreg”, “MultiRead”, “TooBig” condition in the package data, the shape of the input is [1657178, 3], the output of the model is the predicted "pile up" condition, the shape of the input is [1657178, 1]. Since this is a classification problem, we use logistic regression and MLP with L2 regularization and SVM with RBF kernel. 

In logistic regression and MLP, we use Relu as activation function and the loss function is:

$L(\theta) = -\frac{1}{m}[\sum^m_{i = 1}y^{(i)}log h_\theta(x^{(i)}) + (1-y)^{(i)}log (1 - h_\theta(x^{(i)}))]$

where: $h_\theta(x) = log(1 + exp(x))$ is the activation function,x is input and y is output.

Hyper-parameter:
For logistic regression $\lambda$ = 10,  L2 regularization
For MLP $\alpha$ = 0.0001, $\lambda$ = 10,  L2 regularization, hidden_layer_sizes = (20, 4)

In SVM with RBF kernel, the loss function is:

$L(\theta) =C[\sum^m_{i = 1}y^{(i)}cost_1(\theta^Tf^{(i)}) + (1-y)^{(i)}cost_0(\theta^Tf^{(i)})] + \frac{1}{2}\sum^n_{j = 1}\theta^2_j$

where: $f^{i} = exp(-\frac{||x-x^{(i)}||^2}{2\sigma^2})$ for guass kernel, 

Hyper-parameter: C = 2, $\gamma = 100$ where $\gamma = 2\sigma^{-2}$

## 3.5 Outlier Detection

# 4. Dataset and Metric


# 5. Evaluation


# 6. Conclusion


# 7. Roles

