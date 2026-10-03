from pathlib import Path
import hashlib
import json
import shutil
import zipfile

root = Path(__file__).resolve().parent
dist = root / 'dist'
artifact = dist / 'ManaMetal-Tooltip-Columns-1.7.10-1.0.0.jar'
report = root / 'build/client-test/result.txt'
assert 'status=PASS' in report.read_text(encoding='utf8'), 'Client test must pass before packaging'
client = json.loads((root / 'build/client-test/verification.json').read_text(encoding='utf8'))
assert client['artifact_sha256'] == hashlib.sha256(artifact.read_bytes()).hexdigest(), 'Client test used a different JAR'
shutil.copy2(root / 'build/client-test/screenshots/two-columns.png', dist / '分栏效果.png')
bundle = dist / 'ManaMetal-Tooltip-Columns-1.7.10-1.0.0-with-source.zip'
with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as out:
    out.write(root / 'LICENSE', 'LICENSE')
    out.write(root / 'README.md', 'README.md')
    out.write(root / 'LICENSE', 'source/LICENSE')
    out.write(root / 'README.md', 'source/README.md')
    out.write(root / '.gitignore', 'source/.gitignore')
    out.write(root / '.gitattributes', 'source/.gitattributes')
    out.write(artifact, artifact.name)
    out.write(root / '使用说明.md', '使用说明.md')
    out.write(dist / '分栏效果.png', '分栏效果.png')
    for name, source in {
        'client-result.txt': report,
        'build.json': root / 'build/verification.json',
        'client.json': root / 'build/client-test/verification.json',
        'regressions.txt': root / 'build/test-results.txt',
    }.items():
        out.write(source, 'validation/' + name)
    for directory in ('src', 'tests', 'client-tests'):
        for path in sorted((root / directory).rglob('*')):
            if path.is_file() and path.suffix in ('.java', '.py', '.info'):
                out.write(path, 'source/' + path.relative_to(root).as_posix())
    for name in ('build.py', 'build.ps1', 'package.py'):
        out.write(root / name, 'source/' + name)
(dist / 'SHA256SUMS.txt').write_text(''.join(
    hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + path.name + '\n'
    for path in (artifact, bundle)), encoding='ascii')
print(bundle)
