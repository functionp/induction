#-*- coding: utf-8 -*-

from rdf import *
from generate_example import eats

class PajekDataGenerator(object):
    base_domain = 'http://example.org/'
    
    def __init__(self, arc_path, instance_path, class_path, domain_string):
        self.arc_path = arc_path
        self.instance_path = instance_path
        self.class_path = class_path
        self.sub_domain = self.base_domain + domain_string + '/'

    def get_instance_url(self, identifier):
        return URIRef(self.sub_domain + str(identifier) + '/')
        
    def parse_line(self, line, filter=lambda x : x):
        return [filter(element) for element in line.split(" ") if element != ""]
    
    def read_arc_data(self):
        data_source = open(self.arc_path, 'r')
        lines = data_source.readlines()

        filter = lambda x: x.replace('\r\n','')

        arcs = [self.parse_line(line, filter) for line in lines]

        return arcs

    def read_instance_data(self):
        data_source = open(self.instance_path, 'r')
        lines = data_source.readlines()

        filter = lambda x: x.replace('"','').replace('\n','')

        instances = [self.parse_line(line, filter) for line in lines]
        instances = [[instance[0], '_'.join(instance[1:])] for instance in instances]

        return instances

    def read_class_data(self):
        data_source = open(self.class_path, 'r')
        lines = data_source.readlines()

        filter = lambda x: x.replace('\n','')

        classes = [self.parse_line(line,filter) for line in lines]

        return classes

    def generate_rdf(self):
        arcs = pj.read_arc_data()
        instances = pj.read_instance_data()
        classes = pj.read_class_data()
    
        graph = Graph()

        for instance in instances:
            number, name = instance
            instance_uri = self.get_instance_url(number)
            graph.add( (instance_uri, FOAF.name, Literal(name)))

        for arc in arcs:
            number_prey = arc[0]
            number_predetor = arc[1]
            
            uri_prey = self.get_instance_url(number_prey)
            uri_predetor = self.get_instance_url(number_predetor)
            graph.add( (uri_predetor, eats, uri_prey))

        for class_info in classes:
            number = class_info[0]
            class_uri = URIRef(class_info[1])
            instance_uri = self.get_instance_url(number)
            graph.add( (instance_uri, dbo_class, class_uri))

        return graph

    def save_graph(self, graph, path):
        gc = GraphController(graph)
        gc.save_graph(path)
    


if __name__ == "__main__":
    #base_directory = "dataset/foodchain/"
    base_directory = "dataset/foodchain_simplified/"
    
    pj = PajekDataGenerator(base_directory + "source/Mondego.txt",
                            base_directory + "source/Mondego_instances.txt",
                            base_directory + "source/Mondego_classes.txt",
                            'Modego')
    graph = pj.generate_rdf()
    pj.save_graph(graph, base_directory + 'rdf/Mondego.rdf')
    
