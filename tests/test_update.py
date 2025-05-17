import json
import os
import sys
import tempfile
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BPS-client', 'src'))

# Provide dummy modules for optional dependencies used in core
modules = {
    "yaspin": types.ModuleType("yaspin"),
    "pyfiglet": types.ModuleType("pyfiglet"),
    "typer": types.ModuleType("typer"),
    "inquirer": types.ModuleType("inquirer"),
    "markdown_editor": types.ModuleType("markdown_editor"),
    "markdown_editor.web_edit": types.ModuleType("markdown_editor.web_edit"),
    "markdown_editor.editor": types.ModuleType("markdown_editor.editor"),
}

modules["yaspin"].yaspin = lambda *a, **k: None
modules["pyfiglet"].figlet_format = lambda *a, **k: ""
class DummyTyper:
    def __init__(self, *a, **k):
        pass
    def command(self, *a, **k):
        def wrapper(f):
            return f
        return wrapper
    def __call__(self, *a, **k):
        pass
modules["typer"].Typer = DummyTyper
modules["inquirer"].prompt = lambda *a, **k: {}
modules["markdown_editor"].web_edit = modules["markdown_editor.web_edit"]
modules["markdown_editor.editor"].MarkdownDocument = object

for name, mod in modules.items():
    if name not in sys.modules:
        sys.modules[name] = mod

import core

class UpdateConceptTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.tmpdir.name, 'BPS.data.json')
        config = {
            'topics': [{'topic': 't1', 'description': 'd1'}],
            'concepts': [
                {'concept': 'c1', 'maintainers': ['m1'], 'summary': 's1', 'topic': 't1', 'tags': ['tag1']},
                {'concept': 'c2', 'maintainers': ['m2'], 'summary': 's2', 'topic': 't1', 'tags': []},
            ]
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
        self.original = core.BPSConfigFile
        core.BPSConfigFile = self.config_path
        self.client = core.BPSclient()

    def tearDown(self):
        core.BPSConfigFile = self.original
        self.tmpdir.cleanup()

    def test_update_modifies_correct_concept(self):
        self.client.updateConcept('c1', maintainers=['x'], summary='new', tags=['t'])
        # ensure first concept updated
        updated = self.client.getConcept('c1')
        self.assertEqual(updated['maintainers'], ['x'])
        self.assertEqual(updated['summary'], 'new')
        self.assertEqual(updated['tags'], ['t'])
        # ensure second concept untouched
        other = self.client.getConcept('c2')
        self.assertEqual(other['maintainers'], ['m2'])
        self.assertEqual(other['summary'], 's2')

if __name__ == '__main__':
    unittest.main()
