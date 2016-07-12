#-*- coding: utf-8 -*-

#from rdflib import Graph, URIRef, BNode, Literal, Namespace
#from rdflib.namespace import RDF, FOAF, OWL, RDFS
#from rdflib.util import guess_format

from rdf import *

def print_graph(graph):
    for subj, pred, obj in graph:
        print u"({0}, {1}, {2})".format(subj, pred, obj)

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
    def __init__(self, dataset):
        super(PPInferenceSystem, self).__init__(dataset)

    def train(self):
        pass

    def reason(self, subj=None, pred=None, obj=None):
        """
        return triples which are likely to hold in the dataset 
        """
        triples = []
        return triples

    def propagation(self, n, m, subj_q, pred_q, obj_q):
        if n == 0: return int((subj_q, pred_q, obj_q) in self.dataset)

        sum_propagation_value = 0
        for _, pred_t, obj_t in self.dataset.triples((subj_q,  None, None)):
            concept_set = self.get_concept_set_s(m, subj_q, pred_t, obj_t)
            for concept in concept_set:
                sum_propagation_value += self.propagation(n-1,m, conceept, pred_q, obj_q)

        return sum_propagation_value

    def get_concept_set_s(m, subj, pred=None, obj=None):
        concept_set = []
        triples = self.dataset.triples((subj, None, None))
            
        if m == 1:
            for concept, _, _ in triples((None, pred, obj)):
                concept_set.append(concept)
        else:
            concept_prime_set = self.get_concept_set_s(obj, None, None)
            for concept_prime in concept_prime_set:
                for concept, _, _ in triples((None, pred, concept_prime)):
                    concept_set.append(concept) #パスとconceptの組にする　再帰の返り値からパスを作成　
            
        return concept_set
        

    def retrieve(self, subj=None, pred=None, obj=None):
        """
        return triples which are true in the dataset
        """
        return self.dataset.triples((subj, pred, obj))

    def print_dataset():
        print_graph(self.dataset)

    
if __name__ == "__main__":

    rg = GraphController()
    rg.construct_graph('dataset/en/rdf/')
    dataset = rg.graph

    inference_system = PPInferenceSystem(dataset)    

    print_graph(dataset)

