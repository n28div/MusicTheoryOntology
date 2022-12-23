import sys
import os
import argparse
import rdflib
import json
from music21.chord import ChordException
from mto.music21 import convert_chord
import tqdm


if __name__ == "__main__":
  argument_parser = argparse.ArgumentParser()
  argument_parser.add_argument("--prefix", type=str, required=True)
  argument_parser.add_argument("--out", type=str, required=True)
  argument_parser.add_argument("--json", type=str, required=False)
  argument_parser.add_argument("--format", type=str, required=False, default="turtle")
  argument_parser.add_argument("--progress", action='store_true')
  args = argument_parser.parse_args()

  with open(args.json) as f:
    chords = json.load(f)

  graph = rdflib.Graph()
  
  for idx, chord in tqdm.tqdm(list(enumerate(chords.keys())), disable=not args.progress):
    try:
      tmp_graph = convert_chord(chord, args.prefix)
      graph.parse(data=tmp_graph.serialize())
    except Exception as e:
      print("Error parsing ", chord)
  
  graph.serialize(args.out, format=turtle)

  
  
  