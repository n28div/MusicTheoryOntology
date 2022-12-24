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
from itertools import combinations

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
    notes_name = list(map(lambda x: x.name, notes))

    for note_name in notes_name:
      if (MTO_KB[note_name], None, None) not in graph:
        mto_kb_iri = MTO_KB[m21_to_mto_label(note_name)]
        graph.add((mto_kb_iri, RDF.type, MTO["Note"]))
        
        leadsheet_note = m21_to_leadsheet_label(note_name)
        graph.add((mto_kb_iri, RDFS.label, rdflib.Literal(leadsheet_note)))
        graph.add((mto_kb_iri, RDFS.comment, rdflib.Literal(f"{leadsheet_note} Named Note")))

    for note_a, note_b in combinations(notes_name, 2):
      note_a_iri = MTO_KB[m21_to_mto_label(note_a)]
      note_b_iri = MTO_KB[m21_to_mto_label(note_b)]
      graph.add((note_a_iri, OWL.sameAs, note_b_iri))
      graph.add((note_b_iri, OWL.sameAs, note_a_iri))

  print(graph.serialize(format=args.format))
