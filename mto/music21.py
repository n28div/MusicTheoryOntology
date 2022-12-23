"""
This file contains the conversion between music21 concepts to MTO.
"""
import os
import argparse
import re
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib import RDF, RDFS, XSD
from music21.interval import Interval
from music21.note import Note
from music21.pitch import Pitch
from harte.harte import Harte
from urllib.parse import quote

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
MTO_ONT = os.path.join(FILE_DIR, "..", "ont", "mto.ttl")

mto_graph = rdflib.Graph()
mto_graph.parse(MTO_ONT)

namespaces_dict = dict(mto_graph.namespaces())
MTO = rdflib.Namespace(namespaces_dict["mto"])
MTO_KB = rdflib.Namespace(namespaces_dict["mto-kb"])
CHORD = rdflib.Namespace(namespaces_dict["chord"])


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
  
  return MTO[f"{name}Interval"]


def get_mtokb_note(note: Note) -> rdflib.URIRef:
  """
  Get the MTO-KB note of the current note.

  Args:
      note (Note): Input note

  Returns:
      rdflib.URIRef: URI of the input note on the MTO-KB namespace.
  """
  note_name = note.name.replace("-", "b")
  note_mto_kb = mto_graph.value(predicate=RDFS.label, 
                                object=rdflib.Literal(note_name, datatype=XSD.string)) 

  if note_mto_kb == None:
    # MTO only supports one modifier -> get first common enharmonic of this note
    common_enha = note.pitch.getAllCommonEnharmonics(alterLimit=1)[0].name.replace("-", "b")
    note_mto_kb = mto_graph.value(predicate=RDFS.label, 
                                  object=rdflib.Literal(common_enha, datatype=XSD.string)) 

    
  return note_mto_kb


def convert_chord(chord: str, prefix: str) -> rdflib.Graph:
  """
  Convert a chord in Harte format to the MTO representation.

  Args:
      chord (str): Chord in Harte format.
      prefix (str): Prefix of the chord individual.

  Returns:
      rdflib.Graph: Triple graph containing the converted chord.
  """
  chord_graph = rdflib.Graph()

  harte = Harte(chord)
  
  if len(harte.notes) > 0:
    root = harte.root()
    root_m21 = Note(root)
    
    chord_namespace = rdflib.Namespace(prefix)

    chord_IRI = chord_namespace[quote(chord, safe="")]
    chord_graph.add((chord_IRI, RDF.type, CHORD["Chord"]))
    chord_graph.add((chord_IRI, RDFS.label, Literal(chord)))

    # retrieve the MTO-KB note of root
    root_mtokb = get_mtokb_note(root_m21)
    chord_graph.add((chord_IRI, CHORD["root"], root_mtokb))

    for note_m21 in harte.notes:
      note_mtokb = get_mtokb_note(note_m21)

      if note_m21 != root_m21:
        interval = Interval(root_m21, note_m21)
        interval_class = convert_interval(interval)
        chord_graph.add((chord_IRI, CHORD["interval"], interval_class))
        chord_graph.add((chord_IRI, MTO["hasNote"], note_mtokb))

           
  return chord_graph
