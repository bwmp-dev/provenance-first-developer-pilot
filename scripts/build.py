"""Reproducible plugin build for the Provenance first-developer pilot.

Compiles against the public Paper API stubs from an exact, pinned Provenance
toolkit commit (compile-time only; nothing from it is packaged).
"""
import hashlib
import io
import os
import re
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

TOOLKIT_COMMIT = "72d1e6dc0655f6af3622b9343e6cf593e0d05852"
STUBS = "packages/test-fixtures/paper-api-stubs/src/main/java/"

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="first-developer-build-") as temporary:
    stage = Path(temporary)
    url = f"https://codeload.github.com/bwmp-dev/provenance/tar.gz/{TOOLKIT_COMMIT}"
    with urllib.request.urlopen(url, timeout=60) as response:
        archive = tarfile.open(fileobj=io.BytesIO(response.read()), mode="r:gz")
    stub_dir = stage / "stub-src"
    for member in archive.getmembers():
        _, _, relative = member.name.partition("/")
        if member.isfile() and relative.startswith(STUBS) and relative.endswith(".java"):
            target = stub_dir / relative[len(STUBS):]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    stubs, classes = stage / "stubs", stage / "classes"
    stubs.mkdir()
    classes.mkdir()
    stub_sources = sorted(stub_dir.rglob("*.java"))
    sources = sorted((root / "src/main/java").rglob("*.java"))
    assert stub_sources and sources
    subprocess.run(["javac", "--release", "8", "-d", str(stubs), *map(str, stub_sources)], check=True)
    subprocess.run(["javac", "--release", "8", "-cp", str(stubs), "-d", str(classes), *map(str, sources)], check=True)
    files = {p.relative_to(classes).as_posix(): p.read_bytes() for p in classes.rglob("*.class")}
    # The platform keeps one immutable artifact per project and exact SHA-256, so
    # each workflow run stamps distinct manifest bytes.
    run_identity = os.environ.get("GITHUB_RUN_ID", "0") + "." + os.environ.get("GITHUB_RUN_ATTEMPT", "0")
    assert re.fullmatch(r"[0-9]+\.[0-9]+", run_identity)
    manifest = (root / "src/main/resources/plugin.yml").read_text()
    assert manifest.count("version: 1.0.0\n") == 1
    files["plugin.yml"] = manifest.replace("version: 1.0.0\n", "version: 1.0.0+run." + run_identity + "\n").encode()
    output = root / "build/first-developer-pilot.jar"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as jar:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            entry.external_attr = 0o100644 << 16
            jar.writestr(entry, data)
    print(hashlib.sha256(output.read_bytes()).hexdigest() + "  build/first-developer-pilot.jar")
