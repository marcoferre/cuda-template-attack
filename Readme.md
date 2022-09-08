Marco Ferrè - 953544 - marco1.ferre@mail.polimi.it

---

# Project #6: GPU-based implementation of Template Attacks
POLIMI - Embedded Systems 2021/2022

## Description
This project is about performing Template Attacks accellerated via GPU computing following the https://wiki.newae.com/Template_Attacks documentation.

The dataset in our hands is composed by 500 traces of 134016 samples each for 256 keys (that differs only for the first sub-key value).

The goal is to attack a key and try to find the first sub-key value.

## CuPy
The implementation is driven by the choice to use CuPy, a framework that permits to write code that is compatible and agnostic with respect to the platform on which is executed.

This allows to have basically the same code between the CPU and GPU implementation.

# Implementation
The step-by-step implementation is visible in the _cuda-template-attack.ipynb_ a jupyter notebook where, using a single power trace, the actions of **profiling** and **attack** are performed according to the description in the _NewAE Technology_ paper.

Using only one trace, and so only one kind of key, the performances are quite poor: about 30 traces to find the first sub-key value. So the attack requires to perform a profiling on every trace available in the dataset.

For this reason the process is splitted in two different scripts: _Profiling_ and _Attack_

## Profiling

The _profiling.py_ script performs the same action described in the notebook mentioned before but for every trace. Due to the size of the dataset (about 60GB) the traces are loaded individually, processed and congregated in the Averaging phase.

Now that the data on which we have to work have a sustainable size the computation proceed through extracion of the Points of Interest until the Covariance Matrix creation.

At this step we need to loop again all the traces to extract the values, for each Hamming Weight, relative to the POIs.

Once the Covariance Matrix is available, with the Mean Matrix and the list of POIs, is saved to a file in the _data_ folder and the profiling part is over.

## Attack

Loading the data saved before and looping on all the traces the attack is performed to find the first sub-key value of each key.

In the _out.txt_ file are reported all the key attacked with all the attempts to find the correct one and the elapsed time. In addition the average of the attempts and execution time.

# Conclusions
Using all the traces, as expected, the attack requires 1/3 of the attempts to converge.