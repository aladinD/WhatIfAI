# Machine Learning Model Analysis
[[_TOC_]]

# Quick Summary
Predictive time series modeling is a more or less **standard problem** in the field of statistical modeling for which **many different approaches** exist. One of the main goals during the AMI project is to evaluate some of these **candidate model approaches** and to eventually decide for one that suits the project task at hand. This underlying document thus presents a quick & dirty analysis of three possible learning approaches and discusses their respective feasibility.  

# Extreme Learning Machines (ELMs)
One very promising emerging approach to combat **regression and classification problems** is the utilization of **Extreme Learning Machines (ELMs)**. While being not so prominent in traditional ML lectures, ELMs are widely known for a **fairly good accuracy** and **extremely fast performance**. The latter follows from the fact that the respective **pseudo-hidden neuron parameters** (in the following just referred to as hidden) do not need to be tuned during learning and are thus independent of the underlying training data set. More so, the hidden neurons are rather **randomly generated** which consequently implies a **random initialization of its parameters** such as input weights, biases, centers, etc. Still, the universal approximation capability holds, for which an arbitrary model accuracy - supposing that there are enough hidden neurons - can be achieved for the regression/classification task at hand.

The probably most distinct property embedded in the ELM nature is the **non-iterative linear solution** for the respective output weights. This is mainly due to the independence between the input and output weights, unlike in a backpropagation scenario. This ultimately renders ELMs to be very fast compared to similar MLP and SVM solutions. 

Most of the discussed concepts below can be re-read in the following articles: 
* [High-Performance Extreme Learning Machines:
A Complete Toolbox for Big Data Applications](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7140733) 
* [Extreme learning machine: Theory and applications](http://www.di.unito.it/~cancelli/retineu11_12/ELM-NC-2006.pdf) 
* [tfelm: a TensorFlow Toolbox for the Investigation of ELMs and
MLPs Performance](https://csce.ucmss.com/cr/books/2018/LFS/CSREA2018/ICA4128.pdf) 

## ELM Model
ELMs are **fast training methods** for **single layer feed-forward neural networks (SLFN)**. Once again, this is because input weights W and biases b are randomly set and never adjusted. Consequently, the respective output weights β are independent. Furthermore, the **randomness of the input layer weights** improves the generalization property w.r.t. the solution of a linear output layer. The so induced orthogonality leads to almost orthogonal and thus **weakly correlated** hidden layer features. 

In general, we can define an ELM model as follows. Consider a set of N distinct training samples (x_i, t_i) where i ranges between 1 and N. The SLFN output equation with L hidden neurons can then be denoted as

<img src="/documentation/Machine Learning Models/images/SLFN_output.png" alt="SLFN Output Equation" width="200"/>

with φ being the activation function (usually a sigmoid), w_i the input weights, b_i the biases and β_i the respective output weights. Consequently, the relation between the network inputs x_i, the target outputs t_i and the estimated outputs y_i is given by

<img src="/documentation/Machine Learning Models/images/estimated_output.png" alt="Estimated Model Output" width="300"/>

where ε denotes the noise comprised of random noise and certain dependencies on hidden variables excluded from the inputs x_i. This process can be re-examined in below figure.

<img src="/documentation/Machine Learning Models/images/SLFN_process.png" alt="ELM SLFN Process" width="500"/>

## Computation
Before discussing the simple computation technique behind ELMs, it is reasonable to first discuss the processes behind the respective hidden neurons as well as a compact matrix notation. 

### Pseudo-Hidden Neurons
In general, the hidden neurons **transform** the underlying input data into a different representation. This is usually done in two steps:
1) The data is projected into the hidden layer using the input layer weights and biases.
2) The projected data is transformed using a non-linear transformation function. 

In particular, using above **non-linear transformation**, the learning capabilities of the ELM can be greatly **increased**. After transformation, the data in the hidden layers h_I can be used to find the output layer weights. Another **practical advantage** is that the respective transformation functions are not constrained by type, that is they can be selected to be very different and even non-existent. Furthermore, since the neurons are linear, they consequently adapt and learn linear dependencies between data features and targets which happens directly without any nonlinear approximation at all. With that in mind, it becomes clear that the number of neurons **must equal** the number of data features. 

Note however, that other types of neurons have also found application in ELMs such as **RBF neurons** with nonlinear projection functions. These can be used to compute predictions based on similar training data samples in order to solve tasks with some more complex dependencies between data features and targets.

### Compact Matrix Notation
ELMs exhibit a **closed form solution** in which the hidden neurons are comprised in a matrix H. The network structure itself though is not noticable in practice meaning that there is only a **single matrix** that describes the projection between two - usually linear - spaces. The projections for the input (X⋅W) and the output (H⋅β) are connected through a nonlinear transformation as follows.

<img src="/documentation/Machine Learning Models/images/nonlinear_trafo.png" alt="Nonlinear Transformation" width="100"/>

The number of hidden neurons thus consequently **regulates** the size of the matrices W, H and β. However, the network neurons are never treated separately. With different types of hidden neurons, the first projection and transformation are performed **independently** for each type of neuron. Then the resulting sub-matrices H_1 are concatenated along the second dimension. For two types of hidden neurons it follows that 

<img src="/documentation/Machine Learning Models/images/H_1.png" alt="H Notation" width="300"/>

where linear neurons are added by simply copying the inputs into the hidden layer outpus

<img src="/documentation/Machine Learning Models/images/H_2.png" alt="Extended H Notation" width="300"/>

### Solution Computation
In general, ELM problems are usually **over-determined (N>L)** with the number of training data samples being much larger than the number of selected hidden neurons. In all other cases (N<=L), regularization should be used in order to obtain a better generalization performance. 

Nevertheless, a unique solution can be found using the pseudoinverse: 

<img src="/documentation/Machine Learning Models/images/H_solution.png" alt="Solution Computation" width="140"/>

## Conclusion
In order to summarize, ELMs have very promising and efficient properties. They have been proven to be very useful for regression tasks as needed in our project. Nevertheless, there have been some reports on negative effects such as 
* Bad initial randomization
* Speedy performance but low accuracy
* Need of regularization options

In particular, it has to be pointed out that ELMs only operate on **one hidden layer** in contrast to general DL approaches. In order to achieve a very high accuracy and approximation, this might not be necessarily the best performing choice considering the amount of COVID-19 data that we have gathered throughout the collection process. 

Nevertheless, there are two very high-performance **Matlab and Python implementations** in form of **ready-to-use toolboxes** discussed in above articles. They promise automatic model structure selection as well as the application of regularization techniques. Furthermore, many approaches using self-written Python code have emerged online. 

However, the main argument that seems to disqualify ELMs - at least from our user point of view - is that **only one group member** has even had any experience at all using them. Furthermore, even though the concepts of ELMs seem promising and effective, most of the ML experience was simply gained in Python using **TensorFlow and PyTorch**. The goal thus remains to find a time series modeling approach which exploits the vast availability of pre-built functions as found in these aforementioned frameworks.  

# Gaussian Processes (GPs)
Another very promising approach which solves **regressional time series problems** is the use of **Gaussian Processes (GPs)** for which a handful of implementations is given in the **scikit ML library**. In particular, there have already been attempts to model and forecast CO2 emissions using GPs, as done [here](https://stats.stackexchange.com/questions/377999/why-are-gaussian-processes-valid-statistical-models-for-time-series-forecasting). This not only **motivates** to further investigate GPs for our project but also demonstrates a successful application, ultimately rendering this approach as **highly plausible** to achieve our specified project target. 

## GP Model
GPs are a very generic class of **supervised learning methods** which are designed to not only solve **regression but also probabilitsic classification problems**. In general, a GP is a **stochastic process** and thus a collection of random variables, e.g. in the time or space domain. Note that every such finite collection of random variables has a **multivariate normal distribution**, that is every finite linear combination of these random variables is strictly **normally distributed**. As such, every GP can be compactly described by the **joint distribution** of all those random variables and is thus strictly specified by its **mean and covariance functions**.

A GP can be described as a functional mapping of random variables x_i

<img src="/documentation/Machine Learning Models/images/GP_mapping.png" alt="GP Mapping" width="100"/>

with mean function m(x)

<img src="/documentation/Machine Learning Models/images/GP_mean.png" alt="GP Mean" width="100"/>

and covariance function k(x, x')

<img src="/documentation/Machine Learning Models/images/GP_cov.png" alt="GP Covariance" width="240"/>

Most ML algorithms that make use of GPs often apply **lazy learning approaches** in order to measure the **similarity** between the respective evaluation points. To this, the so-called **kernel function** is examined which aids to predict the value for a future, e.g. time series point. The so obtained prediction - in form of a **distribution** - not just provides an estimation but also contains some **uncertainty information** which is embedded in the **one-dimensional Gaussian distribution**. The same holds for multidimensional predictions where the GP is multivariate and for which the respective multivariate Gaussian distributions are the corresponding marginal distributions at the current evaluation point. 

## Pros and Cons
The advantages of GP models can mainly be summarized as follows:
* The model prediction interpolates between the observations for regular kernels.
* The prediction is probabilistic and allows for an analysis of confidence intervals which in turn aids to decide whether refitting is necessary. The latter one can thus be solved in an online fashion. 
* There is a certain versatitlity due to the possibility to choose differently specified kernels. 

However, there are also some severe disadvantages of GP models:
* Non-sparsity: The models use the whole sample space and all feature information in order to perform a prediction.
* Low efficiency in high-dimensional (>12) spaces.

## Conclusion
While GP models bring many different advantages and are also quite broady represented in the desired frameworks to be used during the project, once again **only few group members** have actively dealt with both the **theory and practical implementation** of such models. Thus, diving deeper in the more complex stochastic modeling theory will certainly **take up more time** than we initially desired to give for the ML core development. As such, we decide that more time should be spent **analyzing, optimizing and troubleshooting** the model output which is frankly the more **exhausting** part for a successful model application. Therefore, we live by the notion that the **more simple the model the better**. Since most of the group members have gained considerable experience in DL modeling scenarios, these are to choose and GP models will thus not be further considered.  

# LSTM RNN 
What all above ML approaches have led to is a more or less pre-determined decision for a **DL solution**. In particular, there are many time-series modeling approaches using **recurrent neural networks (RNNs)**. However, while these seem to achieve some **very high accuracies**, they also suffer from severe drawbacks which might also affect our project scope due to the vast amount of data that we have gathered. To be precise, one particularly dangerous disadvantage of conventional RNNs is their **short-term memory capacity**. In order to combat this drawback, **long short-term memory (LSTM) RNNs** have been introduced that incorporate a significantly **greater (longer) memory capacity**. 

Unlike feed-forward neural networks, LSTMs have **feedback connections** and are not only able to process **single data points** but also **entire sequences** - a character trait especially needed for our project implementation! A huge proportion of LSTM associated model applications so far have been based on time series data. In particular, some models - as presented [here](https://www.curiousily.com/posts/time-series-forecasting-with-lstm-for-daily-coronavirus-cases/) - have been constructed that actively address the COVID-19 pandemic and use time-series data for accurate predictions. This once again **motivates** to further discuss LSTM RNNs as a valid approach for our project realization. 

## LSTM core idea
In general, RNNs can be represented in a **chain-like form of repeating modules** which incorporate loops and interconnections. LSTMs in particular introduce a repeating module which has a more advanced structure containing **several neural network layers**. The general chain layout for the repeating module of such LSTMs is depicted below.

<img src="/documentation/Machine Learning Models/images/LSTM_layout.png" alt="LSTM Repeating Module Layout" width="300"/>

<img src="/documentation/Machine Learning Models/images/LSTM_tools.png" alt="LSTM Tools" width="300"/>

The core of LSTM based RNNs is the **cell state C** which is defined by the horizontal line on the top of the respective module:

<img src="/documentation/Machine Learning Models/images/LSTM_cellState.png" alt="LSTM Cell State" width="300"/>

In particular, the cell state interacts **linearly** with other elements throughout its way. The main feature of LSTMs is the ability to **add and remove** certain information w.r.t. the cell state, that is information can be **sequentially** added to and removed from it. This mechanism is regulated by so-called **gates** which will be examined in more detail in the following subsection. 

## LSTM Information Gates
The gate structures are usually composed of **sigmoid neural net layers** and **pointwise multiplication operators**. Depending on their function, we can classify them as forget, input and output gates.

### Forget Gate
The forget gate more or less describes the first decision that the network has to make: What information has to be **thrown away** from the cell state. It thus decides whether information will be **deleted or not**. In order to do so, the gate considers the **previous h_(t-1) and current x_t value**, passes both through the sigmoid layer and computes a value **f_t between 0 and 1** for the current cell state C_t which describes the **memory degree** (0 = forget entirely, 1 = remember entirely).

<img src="/documentation/Machine Learning Models/images/LSTM_forgetGate.png" alt="LSTM Forget Gate" width="400"/>

### Input Gate 
The next consequent step for the LSTM is decide what **new information is going to be added** to the current cell state. This is performed by the input gate which consists of two parts:
* First, a sigmoid layer - the so-called input gate layer - decides which former values will be updated.
* Second, a tanh layer creates a dedicated vector of new candidate values that could be added to the cell state. 

<img src="/documentation/Machine Learning Models/images/LSTM_inputGate_1.png" alt="LSTM Input Gate (1)" width="400"/>

Furthermore, the now old cell state C_(t-1) has to be updated to the new cell state C_t by multiplying the old state with f_t - forgetting the information we decided to forget in the forget gate - and by adding above multiplication of i_t with the candidate vector.

<img src="/documentation/Machine Learning Models/images/LSTM_inputGate_2.png" alt="LSTM Input Gate (2)" width="400"/>

### Output Gate 
Last but not least, the LSTM has to decide **what to output**. This is highly dependent on the cell state and is essentially going to be a **filtered version** of it performed by the output gate:
* First, a sigmoid layer is run for h_(t-1) and x_t analogously to above input gate.
* Second, the current cell state is pushed through a tanh layer which confines a value space between -1 and 1. 
* Third, we multiply each outcome and obtain the consecutive value for h_t which reflects all our previous decisions. 

<img src="/documentation/Machine Learning Models/images/LSTM_outputGate.png" alt="LSTM Output Gate" width="400"/>

## Conclusion
To summarize, LSTM RNNs have a **very high and most importantly proven performance** w.r.t. time series modeling. In particular, there are also **many guides and tutorials** on how to realize and troubleshoot (optimize) LSTM RNNs using Python. Due to their **DL character**, they are furthermore very **familiar** to the group members as multiple layers can and should be constructed. In particular, there is also **no higher effort in understanding** the advanced LSTM architecture and its many variants as they can be **astractly considered** as "just elements in a RNN". As such, LSTM RNNs are currently the most promising solution to the time series model approach that we intend for our project scope. 

A sample realization of LSTM RNNs using Keras in Python is demonstrated [in this article](https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/), a time series weather forecasting guide using LSTMs in Python has been shown [in this approach](https://www.tensorflow.org/tutorials/structured_data/time_series) and above COVID-19 forecast using LSTMs can once again be found [here](https://www.curiousily.com/posts/time-series-forecasting-with-lstm-for-daily-coronavirus-cases/). 

# Decision
  
After having reviewed above candidate ML models that **certainly would all suffice** to achieve the project task at hand, a final decision is hard to make. **LSTM-based RNNs** in particular seem to be a very powerful solution to the problem. Furthermore, the **matureness of LSTMs** compared to Extreme Learning and GP models as well as their **familiarity to every group member** - as they can be seen as an extension to RNNs - are two of the main driving factors fueling the decision for it. However, one major drawback that has emerged throughout the **data collection phase** is that not all of our data sets are of a particularly high quality due to **noise** and other factors. Thus, we believe that performing predictions using LSTM-based RNNs **will not exploit above high-feature advantages** nor will the predictions be of a particularly high accuracy due to the **low-quality data** in some cases. Furthermore, we believe that above candidate approaches need to be compared to more **traditional regression approaches** such as linear regression and decision trees which are well-known to the group members. In particular, necessary obstacles such as **troubleshooting, hyperparameter optimizing and model verification** are well understood for these regression model classes. In conclusion, very powerful model architectures have been discussed and examined. However, the preliminary performance assessment will determine whether complex approaches **outperform** standard regression models. A **final decision** on the model architecture can certainly only be made **after the assessment**.

