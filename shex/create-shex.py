#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 16:19:15 2024

@author: gustavo
"""

from shexer.shaper import Shaper
from shexer.consts import NT, TURTLE

target_classes = [
     "https://schema.org/SearchAction",
     "https://schema.org/Dataset",
     "https://schema.org/Organization"
]

namespaces_dict = {"http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                   "http://www.w3.org/2000/01/rdf-schema#": "rdfs", 
                   "http://weso.es/shapes/": "",
                   "http://www.w3.org/2001/XMLSchema#": "xsd",
                   "http://www.cidoc-crm.org/cidoc-crm/": "cidoc-crm",
                   "http://schema.org/": "schema",
                   "http://rdfs.org/ns/void#": "void",
                   "http://creativecommons.org/ns#": "creativeCommons",
                   "http://purl.org/dc/terms/": "dc-terms",
                   "http://xmlns.com/foaf/0.1/": "foaf",
                   "http://www.w3.org/2004/02/skos/core#": "skos",
                   "http://purl.org/dc/elements/1.1/": "dc",
                   }

input_nt_file = "dataset.ttl"
shaper = Shaper(target_classes=target_classes,
                #raw_graph=raw_graph,
                graph_file_input=input_nt_file,
                #url_endpoint=url_endpoint, 
                input_format=TURTLE,
                limit_remote_instances=5,
                namespaces_dict=namespaces_dict,  # Default: no prefixes
                instantiation_property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type")  # Default rdf:type

output_file = "shex-lod-visual.shex"

shaper.shex_graph(output_file=output_file,
                  acceptance_threshold=0.1)

print("Done!")