"""Run the accompanying retirement-information analysis from its checked archive."""
import hashlib
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ARCHIVE = 'Retirement_information_analysis.zip'
ARCHIVE_SHA256 = 'f52326cd067ef020ecce59210bd2815ec6c53cadbeb140cc3f93ba4b41a8317c'
LOCAL_DIRECTORY = '_omega_analysis'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def checked_target(root, name):
    relative = PurePosixPath(name)
    if (not relative.parts or relative.is_absolute() or '..' in relative.parts
            or '\\' in name or ':' in name or relative.parts[0] != 'retirement-information'):
        raise ValueError('Unsafe archive path: ' + name)
    target = root.joinpath(*relative.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Archive path leaves the extraction directory: ' + name)
    parent = target
    while parent != root.parent:
        if parent.is_symlink() or getattr(parent, 'is_junction', lambda: False)():
            raise ValueError('Extraction through links is not allowed: ' + str(parent))
        if parent != target and parent.exists() and not parent.is_dir():
            raise ValueError('Archive parent is not a directory: ' + str(parent))
        parent = parent.parent
    return target


def extract_checked(archive, root):
    seen = set()
    with zipfile.ZipFile(archive) as source:
        members = source.infolist()
        if sum(m.file_size for m in members) > 1024**3:
            raise ValueError('Archive expansion exceeds the package limit')
        targets = []
        # Validate all paths and existing members before creating files.
        for member in members:
            target = checked_target(root, member.orig_filename)
            key = '/'.join(PurePosixPath(member.orig_filename).parts).casefold()
            if key in seen:
                raise ValueError('Duplicate archive path: ' + member.filename)
            seen.add(key)
            mode = (member.external_attr >> 16) & 0o170000
            if mode not in (0, 0o100000, 0o040000):
                raise ValueError('Special archive member rejected: ' + member.filename)
            if target.exists():
                if member.is_dir():
                    if not target.is_dir():
                        raise ValueError('Existing directory path is a file')
                elif not target.is_file() or digest(target) != hashlib.sha256(source.read(member)).hexdigest():
                    raise ValueError('Existing extracted file differs; keep your changes in a separate directory: ' + str(target))
            targets.append((member, target))
        for member, target in targets:
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            elif not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as output:
                    output.write(source.read(member))
    entry = root / 'retirement-information/reproduce.py'
    if not entry.is_file():
        raise ValueError('Analysis entry point is missing')
    return entry


def prepare(base):
    archive = base / ARCHIVE
    if not archive.is_file() or digest(archive) != ARCHIVE_SHA256:
        raise ValueError('Missing or changed analysis archive: ' + str(archive))
    return extract_checked(archive, base / LOCAL_DIRECTORY)


def main():
    entry = prepare(Path(__file__).resolve().parent)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable, '-B', str(entry), *sys.argv[1:]],
                          cwd=entry.parent, env=env).returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
