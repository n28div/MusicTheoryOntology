import os
import argparse
import rdflib
from rdflib import RDF, RDFS, XSD
from music21.note import Note
from music21.interval import Interval
from harte.harte import Harte
from mto.music21 import convert_interval

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
MTO_ONT = os.path.join(FILE_DIR, "ont", "mto.ttl")

mto_graph = rdflib.Graph()
mto_graph.parse(MTO_ONT)

namespaces_dict = dict(mto_graph.namespaces())
MTO = rdflib.Namespace(namespaces_dict["mto"])
MTO_KB = rdflib.Namespace(namespaces_dict["mto-kb"])
CHORD = rdflib.Namespace(namespaces_dict["chord"])

def get_mtokb_note(note: str) -> rdflib.URIRef:
  """
  Get the MTO-KB note of the current note.

  Args:
      note (str): Input note

  Returns:
      rdflib.URIRef: URI of the input note on the MTO-KB namespace.
  """
  note_mto_kb = mto_graph.value(predicate=RDFS.label, 
                                object=rdflib.Literal(note, datatype=XSD.string))
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
  root = harte.root()
  root_m21 = Note(root)
  
  chord_namespace = rdflib.Namespace(prefix)

  chord_IRI = chord_namespace[chord]
  chord_graph.add((chord_IRI, RDF.type, CHORD["Chord"]))

  # retrieve the MTO-KB note of root
  root_mtokb = get_mtokb_note(root)
  chord_graph.add((chord_IRI, CHORD["root"], root_mtokb))

  for note_m21 in harte.notes:
    note_name = note_m21.name.replace("-", "Flat").replace("#", "Sharp")
    note_mtokb = get_mtokb_note(note_name)
    
    if note_m21 != root_m21:
      interval_bnode = rdflib.BNode()
      interval = Interval(root_m21, note_m21)
      interval_class = convert_interval(interval)
      chord_graph.add((interval_bnode, RDF.type, interval_class))
      chord_graph.add((interval_bnode, MTO["hasNote"], note_mtokb))

      chord_graph.add((chord_IRI, CHORD["interval"], interval_bnode))
      
      
  return chord_graph


if __name__ == "__main__":
  argument_parser = argparse.ArgumentParser()
  argument_parser.add_argument("--prefix", type=str, required=True)
  argument_parser.add_argument("--chord", type=str, required=False)
  args = argument_parser.parse_args()

  converted = convert_chord(args.chord, args.prefix)
  print(converted.serialize(format="ttl"))