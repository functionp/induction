#-*- coding: utf-8 -*-

from rdf import *
from inference import *
import random
import copy
import time
import sys

def get_average(l):
    return sum(l) / float(len(l))

class Experiment(object):
    def __init__(self, rdf_directory, target_predicate, inference_system, removal_rate=0.3):
        rg = GraphController()
        rg.construct_graph(rdf_directory)
        self.graph_original = copy.deepcopy(rg.graph)
        self.graph_experiment = copy.deepcopy(rg.graph)
        self.target_predicate = target_predicate
        self.remove_properties(removal_rate)
        
        self.inference_system = inference_system
        self.inference_system.dataset = self.graph_experiment

    def remove_properties(self, removal_rate):
        for triple in self.graph_experiment.triples((None, self.target_predicate, None)):
            if random.uniform(0,1) <= removal_rate:
                self.graph_experiment.remove(triple)

    def infer_properties(self):
        removed_properties = self.graph_original - self.graph_experiment
        start_time = time.time()
        
        reasoned_triples = []
        for subj, pred, obj in removed_properties:
            reasoned_triples += self.inference_system.reason(subj, pred)

        elapsed_time = time.time() - start_time
        
        reasoned_graph = GraphController.triples_to_graph(reasoned_triples)
        correct_graph = reasoned_graph & removed_properties

        return reasoned_graph, removed_properties, correct_graph, elapsed_time

    def report_result(self, reasoned_graph, removed_properties, correct_graph):
        print "\nCorrect Triples"
        print_graph(removed_properties, 0)

        print "\nInferred Triples"
        print_graph(reasoned_graph, 0)

        self.report_precision_recall(len(reasoned_graph), len(removed_properties), len(correct_graph))

    def report_precision_recall(self, num_reasoned, num_removed, num_correct):
        print "Removed Graph Nodes: {0}".format(num_removed)
        print "Inferred Graph Nodes: {0}".format(num_reasoned)
        print "Correct Graph Nodes: {0}".format(num_correct)
        
        precision = num_correct / float(num_reasoned)
        recall = num_correct / float(num_removed)
        f_value = 2 * precision * recall / float(precision + recall) if precision + recall > 0 else 0

        print "\nPrecision: {0}, Recall: {1}".format(precision, recall)
        print "F Value: {0}".format(f_value)

    def execute_experiment(self):
        reasoned_graph, removed_properties, correct_graph, elapsed_time = self.infer_properties()
        self.report_result(reasoned_graph, removed_properties, correct_graph)

    @classmethod
    def execute_multiple_experiment(cls, rdf_directory, activate_function, n_experiment=10, n=1, m=1):
        removal_rate = 0.15

        recall_list = []
        precision_list = []
        elapsed_time_list = []
        f_value_list = []

        for i in range(n_experiment):
            print "============================"
            print "{0} th experimet".format(i+1)
            
            inference_system = PPInferenceSystem(None, activate_function, n,m)    
            experiment = Experiment(rdf_directory, dbo_class, inference_system, removal_rate)

            reasoned_graph, removed_properties, correct_graph, elapsed_time = experiment.infer_properties()
            if len(reasoned_graph) == 0: continue

            precision = len(correct_graph) / float(len(reasoned_graph))
            recall = len(correct_graph) / float(len(removed_properties))
            
            f_value = 2 * precision * recall / float(precision + recall) if precision + recall > 0 else 0

            recall_list.append(recall)
            precision_list.append(precision)
            f_value_list.append(f_value)
            elapsed_time_list.append(elapsed_time)

            print "Experiment finished in {0} sec.".format(round(elapsed_time,3))

        precision_average = get_average(precision_list)
        recall_average = get_average(recall_list)
        f_value_average = get_average(f_value_list)
        elapsed_time_average = get_average(elapsed_time_list)

        print "============================"
        print "{0} experiments are done." .format(n_experiment)
        print "Average Recall: {0}" .format(recall_average)
        print "Average Precision: {0}" .format(precision_average)
        print "Average F Value: {0}" .format(f_value_average)
        print "Average Time: {0} s" .format(elapsed_time_average)

if __name__ == "__main__":
    rdf_directory = 'dataset/foodchain_simplified/rdf/'
    
    '''
    # this is a code for executing one single experiment
    inference_system = PPInferenceSystem(None, PPInferenceSystem.activate_threshold(0.6), 1, 1)    
    experiment = Experiment(rdf_directory, dbo_class, inference_system, 0.15)
    experiment.execute_experiment()
    '''

    args = sys.argv

    param_dict = {'m': 1, 'n': 1, 'num_experiments':20, 'activation_function': PPInferenceSystem.activate_threshold(0.6)}

    if len(args) >= 2: param_dict['num_experiments'] = int(args[1])
    if len(args) >= 3: param_dict['m'] = int(args[2])
    if len(args) >= 4: param_dict['n'] = int(args[3])
    if len(args) >= 5:
        if args[4] == 'threshold':
            param_dict['activation_type'] = PPInferenceSystem.activate_threshold
            param_dict['activation_function'] = param_dict['activation_type'](0.6)
            type_conversion = float
        else:
            param_dict['activation_type'] = PPInferenceSystem.activate_argmax
            param_dict['activation_function'] = param_dict['activation_type'](2)
            type_conversion = int
    if len(args) >= 6:
        param_dict['activation_function'] = param_dict['activation_type'](type_conversion(args[5]))


    Experiment.execute_multiple_experiment(rdf_directory,
                                           param_dict['activation_function'],
                                           param_dict['num_experiments'],
                                           param_dict['n'],
                                           param_dict['m'])
