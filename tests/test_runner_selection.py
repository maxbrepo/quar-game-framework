import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('qgf_runner', str(Path(__file__).resolve().parents[1] / 'main.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class RunnerTests(unittest.TestCase):
 def test_range(self):
  cases={'001':None,'002':None,'010':None}
  self.assertEqual(r.select_range(cases,'002','010'),['002','010'])
  with self.assertRaises(ValueError):r.select_range(cases,'010','002')
  with self.assertRaises(ValueError):r.select_range(cases,'100','200')
 def test_chapter(self):
  with TemporaryDirectory() as d:
   root=Path(d)
   with patch.object(r,'ROOT',root):
    cases={'001':root/'examples/01 core/001 foo/main.vq','010':root/'examples/02 game loop/010 bar/main.vq'}
    self.assertEqual(r.select_chapter(cases,2),['010'])
    with self.assertRaises(ValueError):r.select_chapter(cases,9)
 def test_classify(self):
  from subprocess import CompletedProcess
  self.assertEqual(r.classify_execution(CompletedProcess([],0,'=== QRVM OUTPUT ===\nProgram executed successfully','')),'PASS')
  self.assertEqual(r.classify_execution(CompletedProcess([],1,'error','')),'FAIL')
  self.assertEqual(r.classify_execution(CompletedProcess([],-11,'','')),'CRASH')
  self.assertEqual(r.classify_execution(CompletedProcess([],1,'','Traceback (most recent call last)')),'CRASH')
if __name__=='__main__':unittest.main()
