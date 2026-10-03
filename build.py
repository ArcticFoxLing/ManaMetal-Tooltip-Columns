from pathlib import Path
import hashlib
import json
import os
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path(os.environ.get('FOXFOX_WORKSPACE', ROOT.parent)).resolve()
BUILD = ROOT / 'build'
CLASSES = BUILD / 'classes'
TESTS = BUILD / 'test-classes'
DIST = ROOT / 'dist'
for folder in (CLASSES, TESTS, DIST):
    folder.mkdir(parents=True, exist_ok=True)
LIBS = WORKSPACE / '.minecraft/libraries'
TARGET = WORKSPACE / '.minecraft/mods/manametalmod-8.0.7.jar'
DEPS = [WORKSPACE / 'FoxFoxAccessories/tools/forge-1.7.10-srg.jar', TARGET,
        LIBS / 'org/ow2/asm/asm-all/5.0.3/asm-all-5.0.3.jar',
        LIBS / 'net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar',
        LIBS / 'org/lwjgl/lwjgl/lwjgl/2.9.1/lwjgl-2.9.1.jar']

def run(args):
    result = subprocess.run(list(map(str, args)), cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, encoding='utf8', errors='replace')
    print(result.stdout, end='')
    with (BUILD / 'test-results.txt').open('a', encoding='utf8') as log:
        log.write(result.stdout)
    result.check_returncode()

(BUILD / 'test-results.txt').write_text('', encoding='utf8')
run(['javac', '--release', '8', '-Xlint:-options', '-encoding', 'UTF-8', '-cp', os.pathsep.join(map(str, DEPS)),
     '-d', CLASSES, *sorted((ROOT / 'src').rglob('*.java'))])
run(['javac', '--release', '8', '-Xlint:-options', '-encoding', 'UTF-8', '-cp', os.pathsep.join(map(str, [CLASSES, *DEPS])),
     '-d', TESTS, *sorted((ROOT / 'tests').rglob('*.java'))])
for test in ('LayoutRegression', 'TransformRegression'):
    run(['java', '-Xverify:all', '-cp', os.pathsep.join(map(str, [TESTS, CLASSES, *DEPS])), test, TARGET])

artifact = DIST / 'ManaMetal-Tooltip-Columns-1.7.10-1.0.0.jar'
with zipfile.ZipFile(artifact, 'w', zipfile.ZIP_DEFLATED) as jar:
    jar.write(ROOT / 'LICENSE', 'META-INF/LICENSE')
    jar.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\n'
                 'FMLCorePlugin: local.manametaltooltip.TooltipColumnsPlugin\r\n'
                 'FMLCorePluginContainsFMLMod: true\r\n\r\n')
    for path in sorted(CLASSES.rglob('*.class')):
        assert int.from_bytes(path.read_bytes()[6:8], 'big') == 52
        jar.write(path, path.relative_to(CLASSES).as_posix())
    jar.write(ROOT / 'src/mcmod.info', 'mcmod.info')
report = {'artifact': artifact.name, 'bytes': artifact.stat().st_size,
          'sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
          'target': TARGET.name, 'target_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(),
          'minecraft': '1.7.10', 'java_bytecode': 8}
(BUILD / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf8')
print(json.dumps(report, indent=2))
