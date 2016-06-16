#-*- coding: utf-8 -*-

from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF, FOAF


bob = URIRef("http://example.org/people/Bob")
linda = BNode() 

name = Literal('Bob') # passing a string
age = Literal(24) # passing a python int
height = Literal(76.5) # passing a python float

n = Namespace("http://example.org/people/")

#n.bob # = rdflib.term.URIRef(u'http://example.org/people/bob')
#n.eve # = rdflib.term.URIRef(u'http://example.org/people/eve')

g = Graph()

g.add( (bob, RDF.type, FOAF.Person) )
g.add( (bob, FOAF.name, name) )
g.add( (bob, FOAF.knows, linda) )
g.add( (linda, RDF.type, FOAF.Person) )
g.add( (linda, FOAF.name, Literal('Linda') ) )

# RDF を指定の形式で出力
#print g.serialize(format='turtle')

g.add( ( bob, FOAF.age, Literal(42) ) )
print "Bob is ", g.value( bob, FOAF.age )

g.set( ( bob, FOAF.age, Literal(43) ) )
print "Bob is now ", g.value( bob, FOAF.age )

# SubjectがBobのノードを全消し
#g.remove( (bob, None, None) ) 

print len(g)

# URLのRDFを読み込む
g2 = Graph()
g2.parse("http://bigasterisk.com/foaf.rdf")

print len(g2)

g.parse("http://bigasterisk.com/foaf.rdf")
print len(g)

#for subj, pred, obj in g2:
#    print "({0}, {1}, {2})".format(subj, pred, obj)
