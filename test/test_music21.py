import pytest
import os
import rdflib
from rdflib import RDF
from music21.interval import Interval

from mto.music21 import convert_interval

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
MTO_ONT = os.path.join(FILE_DIR, "..", "ont", "mto.ttl")

mto_graph = rdflib.Graph()
mto_graph.parse(MTO_ONT)

namespaces_dict = dict(mto_graph.namespaces())
MTO = rdflib.Namespace(namespaces_dict["mto"])
MTO_KB = rdflib.Namespace(namespaces_dict["mto-kb"])
CHORD = rdflib.Namespace(namespaces_dict["chord"])

# at most up to DoubleOctave has been implemented
@pytest.mark.parametrize("interval", list(range(0, 25)))
def test_existing_interval(interval: int):
    """
    Test whether all the intervals from music21 using niceName
    can simply be translated to mto by removing spaces and templating
    it with `has{niceName}Interval`.

    Args:
        interval (int): Interval to be tested as number of semitones from root.
    """
    interval = Interval(interval)
    assert (None, convert_interval(interval), None) in mto_graph