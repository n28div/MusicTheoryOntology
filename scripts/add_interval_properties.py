"""
Script used to add to the ontology the property of each interval.
This is done by taking all the intervals and creating an object property
of the form has<interval name> that has range and domain = mto:Note.

All the properties are then added to the mto-kb notes by leveraging 
the music21 library.
"""
import re
import rdflib
import argparse
import music21

def mto_to_m21_note(note: str) -> str:
  """
  Convert an mto note into a music21 note.
  mto notes use Flat instead of - and Sharp instead
  of #.

  Args:
      note (str): Note in mto format
  Returns:
      str: Note in music21 format.
  """
  note = note.replace("-", "Flat")
  note = note.replace("#", "Sharp")
  return note

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

  # add hasInterval property that will be subclassed by each property
  graph.add((MTO["hasInterval"], RDF.type, OWL.ObjectProperty))
  graph.add((MTO["hasInterval"], RDFS.range, MTO.Note))
  graph.add((MTO["hasInterval"], RDFS.domain, MTO.Interval))

  # create the object properties
  interval_properties = dict()
  for s, _, _ in graph:
    name = str(s).split("/")[-1]

    if (MTO[name], MTO["hasSemitoneCount"], None) in graph:
      property_name = f"has{name}"
      interval_properties[name] = property_name

      graph.add((MTO[property_name], RDF.type, OWL.ObjectProperty))
      graph.add((MTO[property_name], RDFS.subPropertyOf, MTO["hasInterval"]))
      graph.add((MTO[property_name], RDFS.range, MTO.Note))
      graph.add((MTO[property_name], RDFS.domain, MTO.Note))
      
      interval_label = graph.value(MTO[name], RDFS.label).lower()
      label = f"has {interval_label}"
      graph.add((MTO[property_name], RDFS.label, rdflib.Literal(label)))
      
      comment = f"Property to assign the {interval_label} to a note."
      graph.add((MTO[property_name], RDFS.comment, rdflib.Literal(comment)))

  # instatiate the object property for each note
  notes = [str(s).split("/")[-1]  for s, _, _ in graph.triples((None, RDF.type, MTO["Note"]))]
  for note_name in notes:
    m21_note = music21.note.Note(note_name)

    for name, prop in interval_properties.items():
      interval_semitones = int(graph.value(MTO[name], MTO["hasSemitoneCount"])) % 12
      subject_note = mto_to_m21_note(m21_note.name)
      object_note = mto_to_m21_note(m21_note.transpose(interval_semitones).name)
      graph.add((MTO_KB[subject_note], MTO[prop], MTO_KB[object_note]))

  print(graph.serialize(format=args.format))
