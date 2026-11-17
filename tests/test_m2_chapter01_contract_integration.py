"""Static architecture checks only; does not execute Visual Quar or SDL3."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'experimental/marathon2/chapter01'
class ContractIntegration(unittest.TestCase):
 def test_all_dependencies_exist(self):
  for name in ('qgf_lifecycle_guard.vq','qgf_lifecycle_transition.vq','qgf_lifecycle_sequence.vq','qgf_lifecycle_contract.vq'):
   self.assertTrue((P/name).is_file(),name)
 def test_no_duplicate_ffi(self):
  for name in ('qgf_lifecycle_guard.vq','qgf_lifecycle_transition.vq','qgf_lifecycle_sequence.vq','qgf_lifecycle_contract.vq'):
   self.assertNotIn('extern "C"',(P/name).read_text())
 def test_reuses_existing_policy(self):
  text=(P/'qgf_lifecycle_contract.vq').read_text()
  for name in ('qgf_lifecycle_next_action','qgf_lifecycle_action_allowed','qgf_lifecycle_guarded_result','qgf_lifecycle_sequence_consistent'):
   self.assertIn(name+'(',text)
 def test_invalid_action_rejected_by_sequence(self):
  text=(P/'qgf_lifecycle_sequence.vq').read_text()
  self.assertIn('if (qgf_lifecycle_action_allowed(before, action) == false) { return false; }',text)
 def test_no_direct_native_call(self):
  text=(P/'qgf_lifecycle_contract.vq').read_text()
  for name in ('SDL_Init(', 'SDL_Quit(', 'SDL_GetError('):
   self.assertNotIn(name,text)
if __name__=='__main__': unittest.main()
