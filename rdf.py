#-*- coding: utf-8 -*-

from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF, FOAF, OWL, RDFS
from rdflib.util import guess_format
import random
import cPickle
import os

dbo_class = URIRef("http://dbpedia.org/ontology/class")

def remove_overlap(l):
    return list(set(l))

def is_uri(uri):
    return 'http' in uri

def is_dbpedia_resource_uri(uri):
    return is_uri(uri) and 'dbpedia' in uri and 'resource' in uri

def convert_dbpedia_uri_to_rdf_url(uri):
    """ Type changes from URI to string"""
    if is_dbpedia_resource_uri(uri):
        return uri.replace('/resource/','/data/') + '.rdf'
    else:
        return uri
    

class RDFCollector(object):
    def __init__(self, object_conditions=[is_dbpedia_resource_uri]):
        self.object_conditions = object_conditions
        self.visited_uris = []

    def download_rdf(self, url, root_dir="dataset/", file_name='', loading_format=None, saving_format='xml'):
        if loading_format == None: loading_format = guess_format(url)

        graph_controller = GraphController()
        graph_controller.get_graph_from_url(url, loading_format)
        
        if file_name == '': file_name = url.split('/')[-1]
        file_path = root_dir + file_name
        
        graph_controller.save_graph(file_path, saving_format)

    def check_object_conditions(self, obj_uri):
        for condition in self.object_conditions:
            if condition(obj_uri) == False: return False

        return True
        
    def get_related_objects(self, target_rdf_url):
        graph = Graph()
        graph.parse(target_rdf_url)

        triples = self.narrow_relations(graph)
        obj_uri_list = remove_overlap([obj for subj, pred, obj in  triples if self.check_object_conditions(obj)])

        return obj_uri_list

    def collect(self, start_rdf_url):
        related_object_uris = self.get_related_objects(start_rdf_url)
        
        while True:
            reduced_object_uris = list(set(related_object_uris) - set(self.visited_uris))
            print "extracted:{0}, visited:{1}, remained:{2}".format(len(set(related_object_uris)), len(set(self.visited_uris)) , len(reduced_object_uris))
    
            if len(reduced_object_uris) == 0: break
            
            for object_uri in reduced_object_uris:
                print object_uri
                rdf_url = convert_dbpedia_uri_to_rdf_url(object_uri)
                try:
                    self.download_rdf(url=rdf_url, root_dir='dataset/01/')
                except Exception as e:
                    print e

            self.visited_uris += reduced_object_uris
            self.visited_uris = remove_overlap(self.visited_uris)

            related_object_uris = []
            for index in range(len(reduced_object_uris)):
                #index = random.randint(0,len(reduced_object_uris) - 1)
                rdf_url = convert_dbpedia_uri_to_rdf_url(reduced_object_uris[index])
                try:
                    related_object_uris += self.get_related_objects(rdf_url)
                except Exception as e:
                    print "Error in get_related_objects"
                    print e

            related_object_uris = remove_overlap(related_object_uris)

            self.save_visited_uris('visited.pkl')

    def save_visited_uris(self, saving_path):
        with open(saving_path,'wb') as fp:
            cPickle.dump(self.visited_uris, fp)

    def load_visited_uris(self, loading_path):
        with open(loading_path,'r') as fp:
            return cPickle.load(fp)

class AnimalRDFCollector(RDFCollector):

    def narrow_relations(self, graph):
        triples = []

        triples.extend(graph.triples((None, RDF.type, None)))
        triples.extend(graph.triples((None, OWL.sameAs, None)))
        triples.extend(graph.triples((None, OWL.differentFrom, None)))
        triples.extend(graph.triples((None, FOAF.primaryTopicOf, None)))
        triples.extend(graph.triples((None, RDFS.seeAlso, None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/ontology/genus'), None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/ontology/family'), None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/ontology/class'), None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/ontology/phylum'), None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/ontology/kingdom'), None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/property/classis'), None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/ontology/kingdom'), None)))
        triples.extend(graph.triples((None, URIRef('http://dbpedia.org/ontology/kingdom'), None)))

        return triples

class GraphController(object):
    def __init__(self, graph = None):
        if graph == None: graph = Graph()
        self.graph = graph

    def construct_graph(self, directory_path='dataset/01/'):
        """Load rdf files in the directry, and construct graph"""
        print "Loading RDF Files.."
        
        rdf_list = os.listdir(directory_path)
        for rdf_file in rdf_list:
            file_path = directory_path + rdf_file
            try:
                self.graph.parse(file_path)
            except:
                print "Error:" + file_path

    def get_graph_from_url(self, rdf_url, loading_format=None):
        if loading_format == None: loading_format = guess_format(rdf_url)
        self.graph.parse(rdf_url, format=loading_format)
    
    def save_graph(self, file_path, saving_format='xml'):
        output = self.graph.serialize(format=saving_format)

        rdf_file = open(file_path, 'w')
        rdf_file.write(output)

    @classmethod
    def triples_to_graph(cls, triples):
        graph = Graph()
        for triple in triples:
            graph.add(triple)

        return graph

if __name__ == "__main__":
    rc = AnimalRDFCollector()
    #rc.download_rdf(url='http://dbpedia.org/data/House_crow.rdf')
    #rc.download_rdf(url='http://dbpedia.org/data/Little_crow_(bird).rdf')
    #rc.download_rdf(url='http://dbpedia.org/data/Eurasian_jay.rdf')
    #rc.download_rdf(url='http://dbpedia.org/data/Collared_crow.rdf')
    #rc.download_rdf(url='http://dbpedia.org/data/Tyto.rdf')
    #rc.get_related_objects(target_uri='http://dbpedia.org/data/Giant_scops_owl.rdf')
    #rc.collect('http://dbpedia.org/data/Bird.rdf')

    #rg = GraphController()
    #rg.construct_graph('dataset/test2/rdf/')
    
    saving_file_path = directory_path + 'graph.rdf'
    rg.save_graph(saving_file_path)

    # rdf2dot -o test.dot test.rdf;dot -Tpng -o test.png test.dot
    
    rc.download_rdf(url='dataset/animal.ttl', file_name='animal.rdf', loading_format='turtle', saving_format='xml')
