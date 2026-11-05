import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

import new_mod

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent
LEFTOVER_TOKENS = ('templatemod', 'Template Mod', 'TemplateMod', 'template_mod', 'template-mod')
TEXT_SUFFIXES = {'.java', '.kts', '.json', '.toml', '.mcmeta', '.properties', '.md'}


def copy_template(destination):
    shutil.copytree(TEMPLATE_ROOT, destination,
                    ignore=shutil.ignore_patterns('.git', '.gradle', '.idea', 'build', 'run', 'versions', 'scripts', '__pycache__'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def my_mod_names():
    args = new_mod.build_parser().parse_args(['--id', 'my_mod', '--name', 'My Mod', '--package', 'com.example.mymod'])
    return new_mod.ModNames.from_args(args)


def leftovers(root):
    found = []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root).as_posix()
        if relative == 'README.md':
            continue
        found.extend(f'path {relative}: {token}' for token in LEFTOVER_TOKENS if token in relative)
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            text = path.read_text(encoding='utf-8')
            found.extend(f'text {relative}: {token}' for token in LEFTOVER_TOKENS if token in text)
    return found


class NewModTest(unittest.TestCase):
    def test_a_renamed_tree_keeps_no_template_token(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'mod'
            copy_template(root)
            wrapper = digest(root / 'gradle/wrapper/gradle-wrapper.jar')
            icon = digest(root / 'src/main/resources/assets/template_mod/icon.png')

            new_mod.rename_tree(root, my_mod_names(), dry_run=False)

            self.assertEqual([], leftovers(root))
            self.assertTrue((root / 'src/main/java/com/example/mymod/loader/MyModFabric.java').is_file())
            self.assertEqual(wrapper, digest(root / 'gradle/wrapper/gradle-wrapper.jar'))
            self.assertEqual(icon, digest(root / 'src/main/resources/assets/my_mod/icon.png'))

    def test_an_invalid_mod_id_is_rejected_with_its_value(self):
        args = new_mod.build_parser().parse_args(['--id', 'My-Mod', '--name', 'My Mod', '--package', 'com.example.mymod'])

        with self.assertRaisesRegex(ValueError, "'My-Mod'"):
            new_mod.ModNames.from_args(args)

    def test_an_already_renamed_tree_is_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'mod'
            copy_template(root)
            new_mod.rename_tree(root, my_mod_names(), dry_run=False)

            with self.assertRaisesRegex(ValueError, 'already renamed'):
                new_mod.rename_tree(root, my_mod_names(), dry_run=False)


if __name__ == '__main__':
    unittest.main()
