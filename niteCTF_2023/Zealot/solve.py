import angr
import logging

logging.getLogger("angr").setLevel("CRITICAL")
angr.manager.l.setLevel("CRITICAL")
proj = angr.Project("Zealot")
simgr = proj.factory.simgr()
simgr.explore(
    find=lambda s: b"Entered Here" in s.posix.dumps(1),
    avoid=lambda s: b"Leave At Once" in s.posix.dumps(1)
)

if len(simgr.found) > 0:
    print(simgr.found[0].posix.dumps(0))
    exit(0)
else:
    print("Not Found")
