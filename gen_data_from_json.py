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
  argument_parser.add_argument("--progress", action='store_true')
  args = argument_parser.parse_args()

  with open(args.json) as f:
    chords = json.load(f)

  
  chords_dir = os.path.join(args.out, "chords")
  if not os.path.exists(chords_dir):
    os.mkdir(chords_dir)
  
  for idx, chord in tqdm.tqdm(enumerate(chords.keys()), disable=not args.progress):
    try:
      out_graph = convert_chord(chord, args.prefix)
      out_file = os.path.join(chords_dir, f"chord_{idx}.ttl")
      
      if not os.path.exists(out_file):
        out_graph.serialize(out_file)
    except Exception as e:
      print("Error parsing ", chord)

  # merge turtles
  graph = rdflib.Graph()
  for ttl in tqdm.tqdm(os.listdir(chords_dir), disable=not args.progress):
    graph.parse(os.path.join(chords_dir, ttl))
  
  graph.serialize(os.path.join(args.out, "chords.ttl"))

  
  
  