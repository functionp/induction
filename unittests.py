#-*- coding: utf-8 -*-

import unittest
from rdf import *
from inference import *
from generate_example import *

class TestPPIS(unittest.TestCase):

    def setUp(self):
        rg = GraphController()
        rg.construct_graph('dataset/example/')
        self.dataset = rg.graph

    def test_retrieve(self):
        inference_system = PPInferenceSystem(self.dataset)    
        triples = inference_system.retrieve(subj=bird_b, pred=eats)
        
        subj, pred, obj = list(triples)[0]

        self.assertEqual((subj,pred), (bird_b,eats))

    def test_prpagation_0_1(self):
        inference_system = PPInferenceSystem(self.dataset)
        p1 = inference_system.propagation(0, 1, bird_d, RDF.type, bird)
        p2 = inference_system.propagation(0, 1, bird_d, eats, mouse)

        self.assertTrue(p1 == 1 and p2 == 0)

    def test_prpagation_1_1(self):
        inference_system = PPInferenceSystem(self.dataset)
        p1 = inference_system.propagation(1, 1, bird_d, habitat, forest)
        p2 = inference_system.propagation(1, 1, bird_d, habitat, riverside)
        self.assertTrue(p1 < p2)

    def test_prpagation_2_1(self):
        inference_system = PPInferenceSystem(self.dataset)
        p1 = inference_system.propagation(2, 1, bird_d, habitat, forest)
        p2 = inference_system.propagation(2, 1, bird_d, habitat, riverside)

        self.assertTrue(p1 < p2)

    def test_prpagation_1_2(self):
        inference_system = PPInferenceSystem(self.dataset)
        p1 = inference_system.propagation(1, 2, bird_d, habitat, forest)
        p2 = inference_system.propagation(1, 2, bird_d, habitat, riverside)
        self.assertTrue(p1 < p2)

    def test_concept_set_s(self):
        inference_system = PPInferenceSystem(self.dataset)
        concept_path_set1 = inference_system.get_concept_path_set_s(1, bird_a, eats, mouse)
        concept_set2 = [concept for concept, path in inference_system.get_concept_path_set_s(1, bird_a, eats, None)]
        concept_path_set3 = inference_system.get_concept_path_set_s(1, minnow, None, None)
        concept_path_set4 = inference_system.get_concept_path_set_s(2, bird_d, eats, minnow)

        test1 = concept_path_set1[0][0] == bird_c
        test2 = bird_b in concept_set2 and bird_c in concept_set2
        test3 = concept_path_set3[0][0] == perch
        test4 = [(bird_d, eats, minnow), (minnow, RDF.type, fish), (perch, RDF.type, fish), (bird_c, eats, perch)] == concept_path_set4[0][1]
        test5 = bird_c == concept_path_set4[0][0]
        
        self.assertTrue(test1 and test2 and test3 and test4 and test5)
        
    def test_concept_set_o(self):
        inference_system = PPInferenceSystem(self.dataset)
        concept_path_set1 = inference_system.get_concept_path_set_o(1, bird_a, eats, mouse)
        concept_path_set2 = inference_system.get_concept_path_set_o(2, perch, RDF.type, fish)
        concept_path_set3 = inference_system.get_concept_path_set_o(2, mouse, RDF.type, mammal)
        
        test1 = concept_path_set1[0][0] == worm
        test2 = concept_path_set2[0][0] == mammal
        test3 = (concept_path_set3[0][0] == insect and concept_path_set3[1][0] == fish) or (concept_path_set3[1][0] == insect and concept_path_set3[0][0] == fish)
        
        self.assertTrue(test1 and test2 and test3)

    def test_get_possible_objects(self):
        inference_system = PPInferenceSystem(self.dataset)
        possible_objects = inference_system.get_possible_objects(RDF.type)

        test1 = fish in possible_objects and mammal in possible_objects and bird in possible_objects and insect in possible_objects
        test2 = len(possible_objects) == 4

        self.assertTrue(test1 and test2)

    def test_reasoning1(self):
        inference_system = PPInferenceSystem(self.dataset, PPInferenceSystem.activate_argmax(1), 1, 1)
        reasoned_triples = inference_system.reason(bird_d, habitat)[0]

        self.assertTrue(reasoned_triples == (bird_d, habitat, riverside))

    def test_reasoning2(self):
        inference_system = PPInferenceSystem(self.dataset, PPInferenceSystem.activate_argmax(1), 2, 1)
        reasoned_triples = inference_system.reason(bird_d, habitat)[0]1

        self.assertTrue(reasoned_triples == (bird_d, habitat, riverside))


if __name__ == "__main__":
    unittest.main()
