def m21_to_mto_label(note: str) -> str:
  """
  Convert an a music21 note to an mto note.
  mto notes use Flat instead of - and Sharp instead
  of #.

  Args:
      note (str): Note in music21 format
  Returns:
      str: Note in mto format.
  """
  note = note.replace("--", "DoubleFlat")
  note = note.replace("##", "DoubleSharp")
  note = note.replace("-", "Flat")
  note = note.replace("#", "Sharp")
  return note

def m21_to_leadsheet_label(note: str) -> str:
  """
  Convert an a music21 note to a leadsheet note.
  
  Args:
      note (str): Note in music21 format
  Returns:
      str: Note in mto format.
  """
  note = note.replace("-", "b")
  return note
