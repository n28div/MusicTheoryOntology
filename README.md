# Music Theory Ontology

Extension to the music theory ontology presented in A Music Theory Ontology [1].

## Updates

### Additional intervals
24 missing intervals have been added, according to [Intervals on wikipedia](https://en.wikipedia.org/wiki/Interval_(music)), including: *augmented eleventh*, *augmented fourteenth*, *augmented ninth*, *augmented octave*, *augmented tenth*, *augmented thirteenth*, *augmented twelfth*, *diminished eleventh*, *diminished fourteen*, *diminished ninth*, *diminished tenth*, *diminished thirteenth*, *diminished twelfth*, *major fourteen*, *major ninth*, *major tenth*, *major thirteen*, *major thirteenth*, *minor fourteenth*, *minor ninth*, *minor tenth*, *minor thirteenth*, *perfect eleventh*, *perfect twelfth*.

### Additional harmonic intervals
56 new harmonic intervals have been added, including: *augmented triad*, *augmented triad*, *diminished seventh tetrad*, *diminished seventh tetrad*, *diminished triad*, *diminished triad*, *diminished triad*, *dominant eleventh pentad*, *dominant ninth pentad*, *dominant ninth pentad*, *dominant ninth pentad*, *dominant seventh tetrad*, *dominant seventh tetrad*, *dominant seventh tetrad*, *dominant thirteenth pentad*, *eleventh pentad*, *half diminished seventh tetrad*, *half diminished seventh tetrad*, *half diminished seventh tetrad*, *major eleventh pentad*, *major ninth pentad*, *major ninth pentad*, *major ninth pentad*, *major seventh tetrad*, *major seventh tetrad*, *major sixth tetrad*, *major sixth tetrad*, *major thirteenth pentad*, *major triad*, *major triad*, *minor eleventh pentad*, *minor major seventh tetrad*, *minor major seventh tetrad*, *minor major seventh tetrad*, *minor ninth pentad*, *minor ninth pentad*, *minor ninth pentad*, *minor seventh tetrad*, *minor seventh tetrad*, *minor seventh tetrad*, *minor sixth tetrad*, *minor sixth tetrad*, *minor sixth tetrad*, *minor thirteenth pentad*, *minor triad*, *minor triad*, *ninth pentad*, *seventh tetrad*, *sixth tetrad*, *suspended fourth triad*, *suspended fourth triad*, *suspended fourth triad*, *suspended second triad*, *suspended second triad*, *suspended second triad*, *thirteenth pentad*.

### Axiomatization of harmonic intervals
Axiomatization of all harmonic intervals have been performed by using OMRAS2 Chord Ontology [2]. 

To give an idea we will show a simple example: given the chord *C:maj* its individual can be represented (in Turtle syntax) as
```turtle
@prefix mto: <http://purl.org/ontology/mto/> .
@prefix mto-kb: <http://purl.org/ontology/mto/kb/> .
@prefix chord: <http://purl.org/ontology/chord/> .

<C:maj> rdf:type chord:Chord ;
        chord:root mto-kb:C ;
        chord:interval mto:MajorThirdInterval ;
        chord:interval mto:PerfectFifthInterval .
```

we can infer that this is a `MajorTriad` by using the following axiom (in Manchester Syntax)
```
Class: MajorTriad
  ...
  EquivalentTo: (chord:interval value mto:MajorThirdInterval) and (chord:interval value mto:PerfectFifthInterval)
  ...
```

### Leading tone degree
[Leading tone](https://en.wikipedia.org/wiki/Leading-tone) class, entity and object property have been added.

### Note interval properties
For each `Interval` in the ontology a corresponding `:has<interval>` property has been added to the ontology, with domain and range `mto:Note`.
Each property has been added to the corresponding note. The target note has been computed using the music21 [3] library, using the number of semitones of each interval as defined by `mto:hasSemitoneCount`.

## Extension analysis
The final ontology contains a total of 2646 axioms, 1653 more than the original ontology.


[1] [Sabbir M. Rashid, David De Roure, and Deborah L. McGuinness. 2018. A Music Theory Ontology. In Proceedings of the 1st International Workshop on Semantic Applications for Audio and Music (SAAM '18)](http://doi.org/10.1145/3243907.3243913)
[2] [Christopher Sutton, Yves Raimond, Matthias Mauch, 2007. The OMRAS2 Chord Ontology](https://motools.sourceforge.net/chord_draft_1/chord.html#future)
[3] TBD