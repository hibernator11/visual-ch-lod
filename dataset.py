import rdflib

class Dataset():
    def __init__(self):
        self.graph = rdflib.Graph()
        self.graph.parse("dataset.ttl")

    def getEndpoints(self):
        
        query = """
        SELECT DISTINCT ?sparql
        WHERE {
            ?s wdt:P5305 ?sparql
        }"""

        qres = self.graph.query(query)

        endpoints = []
        for row in qres:
            endpoints.append(str(row.sparql))

        return endpoints

    def getSPARQL(self, sparql, type):
        query = """
        prefix dcterms: <http://purl.org/dc/terms/> 
        prefix schema: <https://schema.org/> 
        prefix wdt: <http://www.wikidata.org/prop/direct/> 
        SELECT DISTINCT ?query
        WHERE {{
            ?s wdt:P5305 <{0}> .
            ?s dcterms:hasPart ?searchAction .
            ?searchAction schema:alternateName "{1}" .
            ?searchAction schema:query ?query
        }}""".format(sparql,type)

        qres = self.graph.query(query)

        query = ''
        for row in qres:
            query = str(row.query)

        return query
    

    def getSPARQLListofAuthors(self, sparql):
        return self.getSPARQL(sparql, "authorList")
        
    def getSPARQLListofWorksFromAuthor(self, sparql):
        return self.getSPARQL(sparql, "worksFromAuthorList")
        
    def getSPARQLMetadataFromAuthor(self, sparql):
        return self.getSPARQL(sparql, "authorInfo")
        
    def getSPARQLProperties(self, sparql):
        return self.getSPARQL(sparql, "properties")

    def getSPARQLClasses(self, sparql):
        return self.getSPARQL(sparql, "classes")
        
    def getSPARQLGraph(self, sparql):
        return self.getSPARQL(sparql, "graph")
    
    def getSPARQLDownloadGraph(self, sparql):
        return self.getSPARQL(sparql, "downloadGraph")
