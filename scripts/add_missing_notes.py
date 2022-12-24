"""
Script used to add to the ontology the missing notes from mto-kb,
such as Fb (FFlat in mto terminology).

These are added by making use of music21.
"""
import re
import rdflib
import argparse
import music21
from utils import m21_to_mto_label, m21_to_leadsheet_label

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", type=str, required=True)
args.add_argument("-f", "--format", type=str, required=False, default="ttl", choices=["ttl", "xml"])

if __name__ == "__main__":
  args = args.parse_args()

  MTO = rdflib.Namespace("http://purl.org/ontology/mto/")
  MTO_KB = rdflib.Namespace("http://purl.org/ontology/mto/kb/")
  OWL = rdflib.OWL
  RDF = rdflib.RDF
  RDFS = rdflib.RDFS

  graph = rdflib.Graph()
  graph.parse(args.input)

  for note_idx in range(12):  
    note = music21.pitch.Pitch(note_idx)
    notes = [note] + note.getAllCommonEnharmonics()
    notes_name = map(lambda x: x.name, notes)

    for note_name in notes_name:
      if (MTO_KB[note_name], None, None) not in graph:
        graph.add((MTO_KB[note_name], RDF.type, MTO["Note"]))
        leadsheet_note = m21_to_leadsheet_label(note_name)
        graph.add((MTO_KB[note_name], RDFS.label, rdflib.Literal(leadsheet_note)))
        graph.add((MTO_KB[note_name], RDFS.comment, rdflib.Literal(f"{leadsheet_note} Named Note")))

  print(graph.serialize(format=args.format))
