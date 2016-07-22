from rdf import *

eats = URIRef('http://semanticweb.org/id/Property-3AEats')
habitat = URIRef('http://umbel.org/umbel/rc/Habitat')
forest = URIRef('http://umbel.org/umbel/rc/Forest')
riverside = URIRef('http://ontologi.es/WordNet/class/Riverside')
bird = URIRef('http://purl.org/biodiversity/taxon/Bird')
mammal = URIRef('http://purl.org/biodiversity/taxon/Mammal')
insect = URIRef('http://purl.org/biodiversity/taxon/Insect')
fish = URIRef('http://purl.org/biodiversity/taxon/Fish')
mouse = URIRef('http://ontologi.es/WordNet/class/Mouse-1')
minnow = URIRef('http://ontologi.es/WordNet/class/Minnow-1')
perch = URIRef('http://ontologi.es/WordNet/class/Perch-6')
worm = URIRef('http://umbel.org/umbel/rc/Worm')

bird_a = URIRef("http://example.org/BirdA")
bird_b = URIRef("http://example.org/BirdB")
bird_c = URIRef("http://example.org/BirdC")
bird_d = URIRef("http://example.org/BirdD")

graph = Graph()
graph.add( (bird_a, RDF.type, bird))
graph.add( (bird_a, habitat, forest))
graph.add( (bird_a, eats, worm))
graph.add( (bird_a, eats, mouse))

graph.add( (bird_b, RDF.type, bird))
graph.add( (bird_b, habitat, riverside))
graph.add( (bird_b, eats, worm))
graph.add( (bird_b, eats, minnow))

graph.add( (bird_c, RDF.type, bird))
graph.add( (bird_c, habitat, riverside))
graph.add( (bird_c, eats, mouse))
graph.add( (bird_c, eats, perch))

graph.add( (bird_d, RDF.type, bird))
graph.add( (bird_d, eats, minnow))

graph.add( (worm, RDF.type, insect) )
graph.add( (mouse, RDF.type, mammal) )
graph.add( (perch, RDF.type, fish) )
graph.add( (minnow, RDF.type, fish) )

if __name__ == "__main__":
    gc = GraphController(graph)
    gc.save_graph('dataset/example/example.rdf')

