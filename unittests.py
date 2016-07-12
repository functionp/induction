#-*- coding: utf-8 -*-

import unittest
from rdf import *
from inference import *

class TestPPIS(unittest.TestCase):

    def setUp(self):
        rg = GraphController()
        rg.construct_graph('dataset/en/rdf/')
        self.dataset = rg.graph

    def test_retrieve(self):
        inference_system = PPInferenceSystem(self.dataset)    
        triples = inference_system.retrieve(subj=URIRef("http://dbpedia.org/resource/Tyto"),
                                            pred=URIRef("http://www.w3.org/2002/07/owl#sameAs"))
        subj, pred, obj = list(triples)[0]

        self.assertEqual((subj,pred), (URIRef("http://dbpedia.org/resource/Tyto"), URIRef("http://www.w3.org/2002/07/owl#sameAs")))

    def test_prpagation_0(self):
        inference_system = PPInferenceSystem(self.dataset)
        p1 = inference_system.propagation(0, 1, URIRef("http://dbpedia.org/resource/Tyto"), URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef('http://pt.dbpedia.org/resource/Tyto'))
        p2 = inference_system.propagation(0, 1, URIRef("http://dbpedia.org/resource/Tyto"), URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef('http://dbpedia.org/resource/Giant_scops_owl'))

        self.assertTrue(p1 == 1 and p2 == 0)


class TestPath(unittest.TestCase):

    def setUp(self):
        rg = GraphController()
        rg.construct_graph('dataset/en/rdf/')
        self.dataset = rg.graph

    def test_test(self):
        self.assertEqual(1,1)


if __name__ == "__main__":
    unittest.main()
