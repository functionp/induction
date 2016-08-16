Inference System using Structure-based Property Propagation
===========================================================

## Overview
This is the the codes and the programs for Hiroki Shimada's master thesis "Property Induction using Structure-based Property Propagation".  
  
## Description
This codes include the inference system using the proposed methodology "Structure-based property propagation", which makes inferences of properties using the dataset of RDF graphs.
It also contains the RDF datasets used in the experiments.
  
## Requirement
### Library
* rdflib==4.2.1
  
### Language and Version
Python  2.7.10  
  
## Usage
### Unit Tests
    python unittests.py
  
### Experiments
#### Command
You can execute multiple experiments by following command.
It will report the average result of all the experiments after finishing them.

    python experiment.py <num_of_experiments> <m> <n> <activation_function> <parameter_for_activate>
  
#### Parameters
* *num_of_experiments* : The number of experiments to be executed. The default is 20.
* *m* : Propagation depth. It can be 1 or 2, but 1 is recommended because 2 took much time. The default is 1.
* *n* : Propagation breadth. It can be 1 or 2. 1 is recommended for the same reason as m. The default is 1.
* *activation_function* : The type of activation function. It can be "threshold" or "argmax". The default is threshold.
* *parameter_for_activate* : If activate funciton is threshold, this is scale s (0-1). In the case of argmax, this is k (integer), the number of triples to pick up from the result set.

As for other parameters, they are fixed as follows: a = 1, f(x) = x.
  
#### Examples
The parameters can be omitted. If they are omitted, the default value is applied.

    python experiment.py 10 1 1

    python experiment.py 20 1 1 argmax 3

    python experiment.py 20 1 1 threshold 0.6
  
## Author
Hiroki Shimada (University of Edinburgh)  
Mail: functionp@gmail.com  
