import argparse
import os
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

TEMPLATE_ID = 'template_mod'
PAST_TENSE = {'rewrite': 'rewrote', 'move': 'moved'}
TEXT_SUFFIXES = {'.java', '.kts', '.json', '.toml', '.mcmeta', '.properties', '.md'}
SKIPPED_PATHS = {'.git', '.gradle', '.idea', '.kotlin', 'build', 'run', 'versions', 'out', 'bin', 'classes', 'scripts',
                 'buildSrc/build', 'buildSrc/.gradle', 'buildSrc/.kotlin', 'README.md'}

PATTERNS = {
    'id': r'^[a-z][a-z0-9_]{1,63}$',
    'package': r'^[a-z_][a-z0-9_]*(\.[a-z_][a-z0-9_]*)+$',
    'class_prefix': r'^[A-Z][A-Za-z0-9]*$',
    'artifact': r'^[a-z0-9][a-z0-9._-]*$',
}


@dataclass(frozen=True)
class ModNames:
    id: str
    name: str
    package: str
    class_prefix: str
    artifact: str

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> 'ModNames':
        names = cls(
            id=args.id,
            name=args.name,
            package=args.package,
            class_prefix=args.class_prefix or ''.join(part.capitalize() for part in args.id.split('_')),
            artifact=args.artifact or args.id.replace('_', '-'),
        )
        for field, pattern in PATTERNS.items():
            value = getattr(names, field)
            if not re.fullmatch(pattern, value):
                raise ValueError(f"--{field.replace('_', '-')} must match {pattern}, got '{value}'")
        if not names.name or '"' in names.name or '\\' in names.name:
            raise ValueError(f"--name must be non-empty and contain no '\"' or '\\', got '{names.name}'")
        return names

    def replacements(self) -> dict[str, str]:
        return {
            'com.stalemated.templatemod': self.package,
            'com/stalemated/templatemod': self.package.replace('.', '/'),
            'Template Mod': self.name,
            'TemplateMod': self.class_prefix,
            TEMPLATE_ID: self.id,
            'template-mod': self.artifact,
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Turn the Stalemated Stonecutter template into a new mod.')
    parser.add_argument('--id', required=True, help='mod id, for example my_mod')
    parser.add_argument('--name', required=True, help='display name, for example "My Mod"')
    parser.add_argument('--package', required=True, help='Java package and Maven group, for example com.example.mymod')
    parser.add_argument('--class-prefix', help='prefix of the main classes (default: the id in PascalCase)')
    parser.add_argument('--artifact', help='jar and Maven artifact name (default: the id with dashes)')
    parser.add_argument('--dry-run', action='store_true', help='print the changes without writing them')
    return parser


def template_files(root: Path) -> Iterator[Path]:
    for directory, subdirectories, files in os.walk(root):
        relative_directory = Path(directory).relative_to(root)
        subdirectories[:] = sorted(name for name in subdirectories if (relative_directory / name).as_posix() not in SKIPPED_PATHS)
        for name in sorted(files):
            relative = relative_directory / name
            if relative.as_posix() not in SKIPPED_PATHS:
                yield relative


def rename_tree(root: Path, names: ModNames, dry_run: bool) -> list[tuple[str, str]]:
    properties = root / 'stonecutter.properties.toml'
    if TEMPLATE_ID not in properties.read_text(encoding='utf-8'):
        raise ValueError(f"stonecutter.properties.toml has no '{TEMPLATE_ID}': this tree was already renamed")

    replacements = names.replacements()
    token = re.compile('|'.join(re.escape(old) for old in replacements))

    def replace(value: str) -> str:
        return token.sub(lambda match: replacements[match.group(0)], value)

    changes = []
    for relative in list(template_files(root)):
        if relative.suffix in TEXT_SUFFIXES:
            text = (root / relative).read_bytes().decode('utf-8')
            if token.search(text):
                changes.append(('rewrite', relative.as_posix()))
                if not dry_run:
                    (root / relative).write_bytes(replace(text).encode('utf-8'))
        target = Path(replace(relative.as_posix()))
        if target != relative:
            changes.append(('move', f'{relative.as_posix()} -> {target.as_posix()}'))
            if not dry_run:
                (root / target).parent.mkdir(parents=True, exist_ok=True)
                (root / relative).rename(root / target)
                remove_empty_parents(root, (root / relative).parent)
    return changes


def remove_empty_parents(root: Path, directory: Path) -> None:
    while directory != root and not any(directory.iterdir()):
        directory.rmdir()
        directory = directory.parent


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    try:
        names = ModNames.from_args(args)
        changes = rename_tree(Path(__file__).resolve().parent.parent, names, args.dry_run)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    for action, detail in changes:
        print(f'would {action} {detail}' if args.dry_run else f'{PAST_TENSE[action]} {detail}')
    print(f'{len(changes)} changes. Next: rewrite README.md, delete scripts/ and fill publish.modrinth_id and publish.curseforge_id.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
