# Meeting Summary (07/07/20)
[[_TOC_]]

# Quick Summary
Some elementary steps regarding the third milestone achievement have been adressed and the next week's plan was set. In particular, below key points towards data pre-processing and model evaluation as well as their respective subtasks were discussed.  

# Milestone 3: A Checklist
In order to quickly recall the requirements for milestone three, the main checkpoints are given as follows.

**Title:**  Data Analysis Pipeline
**Due Date:** July 24

**Task Description:** \
    ● Build an operational data processing pipeline, which includes all the essential
        Machine Learning steps that you deem necessary. \
    ● Establish figures of merit, measuring and assessing the quality or relative
        performance of various machine learning models that you may consider as
        candidates.\
    ● Prepare the pipeline to allow for comparing alternative data modelling techniques
        under a common framework for measuring and comparing performance.\
    ● Choose a limited set (candidates) of appropriate Machine Learning models for
        comparison.\
    ● Specify and implement the process of comparing various models on a sound
        scientific basis.\
    ● You can use available Machine Learning frameworks for implementation in
        Python.\
    ● Test and verify your data analysis pipeline using a simple dummy test set.\
    ● Preliminary data analysis of the data pertaining to your research question (no
        optimization, no final decision on model).

**Deliverable:**\
    ● Submit a document describing \
            --> the data processing pipeline\
            --> the set of candidate machine learning models and\
            --> a short summary of your preliminary assessment of candidate ML models.\
    ● A mock-up of a front-end to use and explain the model (design).\
    ● A Python software, implementing a running data analysis pipeline using a simple
       (dummy) test set for testing and verification.

# Time Synchronization
Before discussing any data pre-processing techniques, first the respective time window shall be set and consequently synchronized with all our considered data sets.

To this, Niklas and Martin will investigate the optimal time window of our most "standing out" feature, the socialblade crawler. Setting this particular set as a more or less "reference" once again points out the respective importance of this feature - which probably makes our group somewhat unique compared to the other ones - and thus justifies the decision to decide for a common time basis.

As soon as the time window has been set, **all group members** are advised to adapt their collected data sets to it, that is only data based on the common time basis shall be considered. 

# Data Pre-Processing
After having agreed upon a common data and time basis, data pre-processing can be applied which involves elementary processing methods that **every member deems reasonable**.

In particular, methods such as **PCA**, **z-scoring**, etc. shall be considered. Evidently, some data sets might not need any further processing.

It is of greater importance to **rather quickly finish** the data pre-processing steps considering above requirements for the milestone three deliverable.

# Model Evaluation & Discussion
Although having agreed upon a suitable machine learning (ML) model - or better say idea - already, AMI further demands us to compare and assess some possible (algorithmic) realizations.

**Let's quickly recall Mike's proposal:** 
>The underlying data sets are split up into two different time windows: pre and post corona-start. 
>
>The former data set is used to train a ML model which is able to sufficiently characterize and predict the model outcome (internet traffic, social media, porn consumption, etc.) for a scenario where the corona pandemic did not occur. By doing this, we can very clearly address the **impact of corona** through the respective error between the obtained data sets and the predicted model output. This can be nicely demonstrated in the final web-interface as a "first step" before further manipulating the corona data. 
>
>Based on this model, its outcome and the respective error metric, the later data set shall be used to train a model that allows for a prediction of the actual outcome for the current corona pandemic. Assuming that is has been sufficiently trained, it is in theory also able to predict a - more or less realistic - outcome for e.g. worse case numbers, higher infection rates etc. which fulfills the original research task. The variation in the **corona abfuck degree** can be nicely implemented into the web-interface and allows the user to interact with the model. 
>
>In summary, two models are effectively being trained where the first predicts a future without corona and the second one with it.

**To Do's** \
In order to be able to realize Mike's proposal, every group member is advised to reflect upon possible ML implementations and methods. To this, **Recurrent Neural Networks (RNNs)** and other time series predictors can be analyzed. In particular, it might make sense to have a look at some very advanced concepts that have not been yet adressed in the AMI sessions. Thus might show that our group has considered some fancy concepts and thus performed intensive research.

It can be helpful to make a **pro-con list** which will aid to the explanation of why the final model was eventually chosen as it is. Furthermore, think of some reasonable figures of merit that will help to identifiy the quality of the model.

In particular, it is important to discuss these models next week in order to quickly progress with the deliverable as this report might take longer due to some more intensive argumentation. Also, **no more than three** different approaches shall be discussed.

# Work Assignment

**In summary:**  
    ●  Set a time window\
    ●  Adapt all relevant data sets to it\
    ●  Data pre-processing\
    ●  ML model evaluation & discussion
    
**Next group session:** July 14
