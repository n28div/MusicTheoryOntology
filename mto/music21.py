"""
This file contains the conversion between music21 concepts to MTO.
"""
from rdflib import Namespace, URIRef
from music21.interval import Interval
import re

MTO = Namespace("http://purl.org/ontology/mto/")
MTO_KB = Namespace("http://purl.org/ontology/mto/kb/")

def convert_interval(interval: Interval) -> URIRef:
  """
  Converts a music21 interval to the corresponding MTO ObjectProperty IRI.

  Args:
      interval (Interval): music21 input interval.

  Returns:
      URIRef: Identifier of the object property of the specified interval.
  """
  name = interval.niceName.replace(" ", "")
  if "-" in name:
    name = re.sub(r"-(\w)", lambda g: g.group().upper(), name)
    name = name.replace("-", "")
  
  return MTO[f"has{name}Interval"]
  