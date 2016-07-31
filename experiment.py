#-*- coding: utf-8 -*-

from rdf import *
from inference import *
import random
import copy
import time

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
        f_value = 2 * precision * recall / float(precision + recall)

        print "\nPrecision: {0}, Recall: {1}".format(precision, recall)
        print "F Value: {0}".format(f_value)

    def execute_experiment(self):
        reasoned_graph, removed_properties, correct_graph, elapsed_time = self.infer_properties()
        self.report_result(reasoned_graph, removed_properties, correct_graph)

    @classmethod
    def execute_multiple_experiment(cls, n_experiment=10, n=1, m=1):
        rdf_directory = 'dataset/foodchain_simplified/rdf/'

        recall_list = []
        precision_list = []
        elapsed_time_list = []
        f_value_list = []

        for i in range(n_experiment):
            inference_system = PPInferenceSystem(None, PPInferenceSystem.activate_argmax, n,m)    
            experiment = Experiment(rdf_directory, dbo_class, inference_system, 0.15)

            reasoned_graph, removed_properties, correct_graph, elapsed_time = experiment.infer_properties()
            if len(reasoned_graph) == 0: continue

            precision = len(correct_graph) / float(len(reasoned_graph))
            recall = len(correct_graph) / float(len(removed_properties))
            
            f_value = 2 * precision * recall / float(precision + recall) if precision + recall > 0 else 0

            recall_list.append(precision)
            precision_list.append(recall)
            f_value_list.append(f_value)
            elapsed_time_list.append(elapsed_time)

        precision_average = get_average(precision_list)
        recall_average = get_average(recall_list)
        f_value_average = get_average(f_value_list)
        elapsed_time_average = get_average(elapsed_time_list)

        print "{0} experiments are done." .format(n_experiment)
        print "Average Precision: {0}" .format(precision_average)
        print "Average Recall: {0}" .format(recall_average)
        print "Average F Value: {0}" .format(f_value_average)
        print "Average Time: {0} s" .format(elapsed_time_average)

if __name__ == "__main__":
    #inference_system = PPInferenceSystem(None, PPInferenceSystem.activate_augmax, 1, 1)    
    #rdf_directory = 'dataset/foodchain_simplified/rdf/'
    #experiment = Experiment(rdf_directory, dbo_class, inference_system, 0.1)
    #experiment.execute_experiment()

    Experiment.execute_multiple_experiment(20,1,1)
