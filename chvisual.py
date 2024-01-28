from SPARQLWrapper import SPARQLWrapper, JSON, XML
from collections import Counter
import networkx as nx
import json
from dataset import Dataset

class CHData():
    def __init__(self, sparql, limit=100):
        self.limit = limit
        self.limitProperties = 1000
        self.sparqlText = sparql
        self.sparqlEndpoint = SPARQLWrapper(sparql)
        self.sparqlEndpoint.setReturnFormat(JSON)
        self.depictions = ['http://xmlns.com/foaf/0.1/depiction']
        self.authornode = ['http://xmlns.com/foaf/0.1/Person', 'http://schema.org/Person']
        self.manifestationnode = ['http://rdaregistry.info/Elements/c/#C10007', 'http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation']
        self.worknode = ['http://rdaregistry.info/Elements/c/#C10001', 'http://rdvocab.info/uri/schema/FRBRentitiesRDA/Work', 'http://schema.org/Work', 'http://schema.org/Book', 'http://schema.org/CreativeWork']
        self.conceptnode = ['http://www.w3.org/2004/02/skos/core#Concept']
        self.dataset = Dataset()

    def getAuthors(self):
        self.sparqlEndpoint.setReturnFormat(JSON)
        textQuery = self.dataset.getSPARQLListofAuthors(self.sparqlText)
        self.sparqlEndpoint.setQuery(textQuery.format(self.limit))
        
        authors = []
        try:
            ret = self.sparqlEndpoint.queryAndConvert()
        
            for r in ret["results"]["bindings"]:
                authors.append(r['name']['value'] + ' - ' + r['author']['value'])
               
        except Exception as e:
            print(e)

        return authors

    
    def getAuthorInfo(self, author):
        self.sparqlEndpoint.setReturnFormat(JSON)
        textQuery = self.dataset.getSPARQLMetadataFromAuthor(self.sparqlText)
        self.sparqlEndpoint.setQuery(textQuery.format(author))

        author = []
        try:
            ret = self.sparqlEndpoint.queryAndConvert()
            author = ret["results"]["bindings"]
                       
        except Exception as e:
            print(e)

        return author

    def getClasses(self):
        self.sparqlEndpoint.setReturnFormat(JSON)
        textQuery = self.dataset.getSPARQLClasses(self.sparqlText)
        self.sparqlEndpoint.setQuery(textQuery.format(self.limit))

        result = []
        classes = []
        vocabs = []
        try:
            ret = self.sparqlEndpoint.queryAndConvert()

            for r in ret["results"]["bindings"]:
                classValue = r['class']['value']
                if '#' in classValue: 
                    vocabValue = classValue[0:classValue.rindex('#')+1]
                else: 
                    vocabValue = classValue[0:classValue.rindex('/')]
                classes.append(classValue)
                vocabs.append(vocabValue)
           
            result.append(classes)
            result.append(Counter(vocabs))
            
        except Exception as e:
            print(e)

        return result

    def getProperties(self):
        self.sparqlEndpoint.setReturnFormat(JSON)
        textQuery = self.dataset.getSPARQLProperties(self.sparqlText)
        self.sparqlEndpoint.setQuery(textQuery.format(self.limitProperties))

        result = []
        vocabs = []
        properties = []
        try:
            ret = self.sparqlEndpoint.queryAndConvert()
        
            for r in ret["results"]["bindings"]:
                propertyValue = r['p']['value']
                if '#' in propertyValue: 
                    vocabValue = propertyValue[0:propertyValue.rindex('#')+1]
                else: 
                    vocabValue = propertyValue[0:propertyValue.rindex('/')]
                properties.append(propertyValue)
                vocabs.append(vocabValue)
           
            result.append(properties)
            result.append(Counter(vocabs))
               
        except Exception as e:
            print(e)

        return result
        
    def getDepiction(self,author):
        for r in author:
            if r['p']['value'] in self.depictions:
                url = r['o']['value']
                url = url.replace("%2520", "_")
                url = url.replace("%252C", ",")
                
                if url.endswith('.thumbnail'):
                    url = url + '.jpeg'
               
                return url

    def getGraph(self,author):
        self.sparqlEndpoint.setReturnFormat(JSON)
        textQuery = self.dataset.getSPARQLGraph(self.sparqlText)
        self.sparqlEndpoint.setQuery(textQuery.format(author))
        ret = self.sparqlEndpoint.queryAndConvert()

        G = nx.Graph()
        for r in ret["results"]["bindings"]:
            #print(r['o']['value'])
            if r['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                if r['o']['value'] in self.authornode:
                    G.add_node(r['o']['value'], nodetype="green", label='author class')
                elif r['o']['value'] in self.worknode:
                        G.add_node(r['o']['value'], nodetype="red", label='work class')
                elif r['o']['value'] in self.manifestationnode:
                        G.add_node(r['o']['value'], nodetype="magenta", label='manifestation class')
                elif r['o']['value'] in self.conceptnode:
                    G.add_node(r['o']['value'], nodetype="cyan", label='concept class')
            else:
                if r['o']['value'] not in author:
                     G.add_node(r['o']['value'], nodetype="blue", label='other')
        
            if r['s']['value'] in author:
                G.add_node(r['s']['value'], nodetype="yellow", label='author node')
            else:
                G.add_node(r['s']['value'], nodetype="blue", label='other')
            
            #add edge
            G.add_edge(r['s']['value'], r['o']['value'])
            
        return G

    def downloadGraph(self,author):
        self.sparqlEndpoint.setReturnFormat(JSON)
        textQuery = self.dataset.getSPARQLDownloadGraph(self.sparqlText)
        self.sparqlEndpoint.setQuery(textQuery.format(author))

        ret = self.sparqlEndpoint.queryAndConvert()

        with open('output/data.json', 'w') as f:
            json.dump(ret,f)

        return "Data downloaded"

    def getAuthorWorks(self, author):
        self.sparqlEndpoint.setReturnFormat(JSON)
        textQuery = self.dataset.getSPARQLListofWorksFromAuthor(self.sparqlText)
        self.sparqlEndpoint.setQuery(textQuery.format(author))

        works = []
        try:
            ret = self.sparqlEndpoint.queryAndConvert()
            works = ret["results"]["bindings"]
                       
        except Exception as e:
            print(e)

        return works
