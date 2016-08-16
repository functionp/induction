#-*- coding: utf-8 -*-

#from rdflib import Graph, URIRef, BNode, Literal, Namespace
#from rdflib.namespace import RDF, FOAF, OWL, RDFS
#from rdflib.util import guess_format

import operator
from math import sqrt
from rdf import *

def remove_overlap(l):
    return list(set(l))

def print_graph(graph, sort_key=None):

    if sort_key != None:
        node_list = []
        for node in graph:
            node_list.append((str(node[sort_key]), node))

        node_list.sort(key=lambda x: x)
        
        graph = [node[1] for node in node_list]

    for subj, pred, obj in graph:
        print u"({0}, {1}, {2})".format(subj, pred, obj)

def length_generator(generator):
    length = 0
    for element in generator:
        length += 1

    return length

        
class Path(object):
    def __init__(self, triples_list):
        self.triples_list = triples_list

        if self.is_this_path() == False: raise Exception

    def is_this_path(self):
        triples_list_length = len(self.triples_list)
        for i in range(triples_list_length):
            subj1, pred1, obj1 = self.triples_list[i]

            if i+1 < triples_list_length: 
                subj2, pred2, obj2 = self.triples_list[i+1]

            if i+2 < triples_list_length: 
                subj3, pred3, obj3 = self.triples_list[i+1]

            # is it connected?
            if not(subj1 == subj2 or subj1 == obj2 or obj1 == subj2 or obj1 == obj2): return False

        return True
            
        
class RDFInferenceSystem(object):
    def __init__(self, dataset):
        self.dataset = dataset

class PPInferenceSystem(RDFInferenceSystem):
    def __init__(self, dataset, activate_function=None, depth=1, breadth=1):
        if activate_function == None: activate_function = PPInferenceSystem.activate_argmax

        self.activate_function = activate_function
        self.depth = depth
        self.breadth = breadth
        super(PPInferenceSystem, self).__init__(dataset)

    def train(self):
        pass

    def get_possible_objects(self, pred):
        return remove_overlap([obj for subj, _, obj in self.dataset.triples((None, pred, None))])
    
    def activate_o_p(self, subj_q=None):
        pass

    def activate_o(self, subj_q, pred_q):
        possible_objects = self.get_possible_objects(pred_q)
        value_pair_list = []

        for possible_object in possible_objects:
            propagation_value = self.propagation(self.depth, self.breadth, subj_q, pred_q, possible_object)
            possible_triple = (subj_q, pred_q, possible_object)
            value_pair_list.append((propagation_value, possible_triple))

        # activate function chooses some triples in the list
        return self.activate_function(value_pair_list) 

    def reason(self, subj_q, pred_q=None, obj_q=None):
        """
        return triples which are likely to hold in the dataset 
        """
        reasoned_triples = []

        if subj_q != None and pred_q != None and obj_q ==  None:
            reasoned_triples = self.activate_o(subj_q, pred_q)
        elif pred_q != None and andpred_q == None and obj_q ==  None:
            reasoned_triples = self.activate_o_p(subj_q)
        elif pred_q == None and andpred_q != None and obj_q !=  None:
            pass

        return reasoned_triples

    def propagation(self, n, m, subj_q, pred_q, obj_q):
        if n == 0: return int((subj_q, pred_q, obj_q) in self.dataset)
    
        sum_outbound_propagation_value = 0
        for _, pred_t, obj_t in self.dataset.triples((subj_q,  None, None)):
            concept_path_set = self.get_concept_path_set_s(m, subj_q, pred_t, obj_t)
            
            for concept, path in concept_path_set:
                sum_outbound_propagation_value += self.propagation(n-1,m, concept, pred_q, obj_q) * self.get_weight(path)

        sum_inbound_propagation_value = 0
        for subj_t, pred_t, _ in self.dataset.triples((None,  None, subj_q)):
            concept_path_set = self.get_concept_path_set_o(m, subj_t, pred_t, subj_q)

            for concept, path in concept_path_set: #refactoring
                sum_inbound_propagation_value += self.propagation(n-1,m, concept, pred_q, obj_q) * self.get_weight(path)
        
        return sum_outbound_propagation_value + sum_inbound_propagation_value

    def get_weight(self, path, a=1, f=lambda x: x):
        if len(path) == 0:
            return 1
        elif len(path) == 1:
            subj, pred, obj = path[0]
            number_of_members = length_generator(self.dataset.triples((None, pred, obj))) or 0.5
            return float(a) / f(number_of_members)
        else:
            path_head = path[0:1]
            path_middle = path[1:-1]
            path_tail = path[-1:]
            return self.get_weight(path_head,a,f) * self.get_weight(path_middle,a,f) * self.get_weight(path_tail,a,f)


    def get_concept_path_set_s_0(self, subj, pred, obj, path_default=[], path_obj=None):
        concept_path_set = []

        for concept, pred_s, obj_s in self.dataset.triples((None, pred, obj)):
            # this condition is only for 1-order path
            if len(path_default) == 0:
                if (subj, pred_s, obj_s) not in self.dataset:
                    continue
            if concept == subj: continue

            # when path is one-order, obj of path is always obj_s
            if path_obj == None: path_obj = obj_s

            path = [(subj, pred_s, path_obj)] + path_default + [(concept, pred_s, obj_s)]
            concept_path = (concept, path)

            if concept_path in concept_path_set: continue

            concept_path_set.append((concept, path))

        return concept_path_set

    def get_concept_path_set_s(self, m, subj=None, pred=None, obj=None):
        concept_path_set = []

        if m == 1:
            concept_path_set = self.get_concept_path_set_s_0(subj, pred, obj)
        else:
            concept_prime_set = self.get_concept_path_set_s(m-1, obj, None, None)
            for concept_prime, path_prime in concept_prime_set:
                concept_path_set += self.get_concept_path_set_s_0(subj, pred, concept_prime, path_prime, obj)

            # unify with the concept set with lower order
            lower_order_set = self.get_concept_path_set_s(m-1, subj, pred, obj)
            concept_path_set = self.unify_concept_path_set(concept_path_set, lower_order_set)

        return concept_path_set
            

    def get_concept_path_set_o_0(self, subj, pred, obj, path_default=[], path_subj=None):
        concept_path_set = []

        for subj_s, pred_s, concept in self.dataset.triples((subj, pred, None)):
            # this condition is only for 1-order path
            if len(path_default) == 0:
                if (subj_s, pred_s, obj) not in self.dataset:
                    continue
            if concept == obj: continue

            # when path is one-order, obj of path is always obj_s
            if path_subj == None: path_subj = subj_s

            path = [(path_subj, pred_s, obj)] + path_default + [(subj_s, pred_s, concept)]
            concept_path = (concept, path)

            # avoid overlapping
            if concept_path in concept_path_set: continue

            concept_path_set.append((concept, path))

        return concept_path_set

    def get_concept_path_set_o(self, m, subj=None, pred=None, obj=None):
        concept_path_set = []

        if m == 1:
            concept_path_set = self.get_concept_path_set_o_0(subj, pred, obj)
        else:
            concept_prime_set = self.get_concept_path_set_o(m-1, None, None, subj)
            for concept_prime, path_prime in concept_prime_set:
                concept_path_set += self.get_concept_path_set_o_0(concept_prime, pred, obj, path_prime, subj) # ほんとに_0でおk？

            # unify with the concept set with lower order
            lower_order_set = self.get_concept_path_set_o(m-1, subj, pred, obj)
            concept_path_set = self.unify_concept_path_set(concept_path_set, lower_order_set)

        return concept_path_set

    def unify_concept_path_set(self,present_set, new_set):
        for new_concept_path in new_set:
            if new_concept_path not in present_set: present_set.append(new_concept_path)
        return present_set

    def retrieve(self, subj=None, pred=None, obj=None):
        """
        return triples which are true in the dataset
        """
        return self.dataset.triples((subj, pred, obj))

    def print_dataset():
        print_graph(self.dataset)

    @classmethod
    def activate_argmax(cls, n=1):

        def activate_function(pairs):
            sorted_pairs = sorted(pairs, key=operator.itemgetter(0), reverse=True)[:n]
            return [pair[1] for pair in sorted_pairs]

        return activate_function

    @classmethod
    def activate_threshold(cls, scale=0.9):

        def activate_function(pairs):
            sorted_pairs = sorted(pairs, key=operator.itemgetter(0), reverse=True)
            max_value = sorted_pairs[0][0]
            threshold = max_value * scale

            return [pair[1] for pair in sorted_pairs if pair[0] >= threshold]

        return activate_function

    
if __name__ == "__main__":

    rg = GraphController()
    rg.construct_graph('dataset/en/rdf/')
    dataset = rg.graph

    inference_system = PPInferenceSystem(dataset)    

    print_graph(dataset)

