# ML Modeling Progress

## Table of Contents
[[_TOC_]]

## Member Attendances
The following members are on vacation and thus not present:

* Max Putz: 20.8. - 3.9. (not available)
* Aron: 22.9. - 5.9. (still available)

## Quick Summary
This underlying document summarizes measures and ideas for the current ML modeling process which were agreed upon in the first meeting. In particular, it highlightens the **four main categories** as well as the respective **responsible group members**.

## Status
**Next Meeting:** Thursday, 20.8. @1.30pm

**To Do**

*General*
- [x] Create an ML Overview Document

*Step 1*
- [ ] ELM model trained and validated
- [ ] Creme model trained and validated
- [ ] Prophet model trained and validated

*Step 2*
- [ ] Defined what to do exactly
- [ ] ...

*Step 3*
- [ ] Cross-validation data set determined
- [ ] Cross-validation data set created
- [ ] ...

*Step 4*
- [ ] Integration parameters defined
- [ ] ...

## 1 Model Architecture Development
In order to catch up on the **clearly failed tasks of Milestone 3**, we compare **three different model approaches** from which we are sure that reasonably good approximations w.r.t. overfitting, etc. are definitely possible.  

The models are all trained and validated on the **four core data sets**:
* Stock Market 
* Internet Exchanges (IX)
* Twitch
* Playstation

This way, we also intend to **compare** different approaches for different data sets, another aspect initially **expected in Milestone 3**.

### ELMs
* Responsibility: **Michael Brandner**
* Modeling is pursued using Extreme Learning Machines: [General ELM Architecture](/documentation/Machine Learning Models/MachineLearningModels.md) 

### Online Learning 
* Responsibility: **Alexander Griessel**
* Online modeling is pursued using [creme](https://creme-ml.github.io/).

**What is creme?**
>creme is a Python library for online machine learning. All the tools in the library can be updated with a single observation at a time, and can therefore be used to learn from streaming data. This is general-purpose library, and therefore caters to different machine learning problems, including regression, classification, and unsupervised learning.

### Time-Series Forecasting 
* Responsibility: **Aron Endres**
* Time-series modeling is pursued using [Prophet](https://facebook.github.io/prophet/)

**What is Prophet?**
>Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. It works best with time series that have strong seasonal effects and several seasons of historical data. Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

>Prophet is open source software released by Facebook’s Core Data Science team. It is available for download on CRAN and PyPI.

## 2 Data Processing
Essential data processing & preparation regarding things like **time window size**, etc. has to be undergone before any of above models are applied. This way, a somewhat unitary data base is used for comparison. 

* Responsibility: **Henrique Frutuoso**
* The main files to be considered in this step are already pushed, see */res/inference*

## 3 Cross-Validation
Estimated model outputs need to be cross-validated. The main strategy is still **undetermined and tba**, though every model analyst in *Step 1* is recquired to firstly cross-validate on their own. In *Step 3* we want to **compare** the respective models on a unified cross-validation data set. This way, we can imply - as mentioned above - which model architecture would perform **better (or worse)** for Stock Market, IX, Twitch and Playstation data sets. 

* Responsibility: **Henrique Frutuoso, Aladin Djuhera**

## 4 Integration
In order to **seamlessly integrate** the mathematical models to the web-interface, integration needs to be defined beforehand, i.e. essential parameters such as time windows, etc. need to be communicated. In other words, front- and back-end need to be properly defined and connected. 

* Responsibility: **Niklas Landerer**
