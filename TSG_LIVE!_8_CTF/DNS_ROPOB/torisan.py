#!/usr/bin/env python3
import angr
import logging

logging.getLogger("angr").setLevel("CRITICAL")
angr.manager.l.setLevel("CRITICAL")
proj = angr.Project("./dns_ropob")

simgr = proj.factory.simgr()
simgr.explore(find=lambda s: b"correct!" in s.posix.dumps(1))
if len(simgr.found) > 0:
    found = simgr.found[0].posix.dumps(0).decode("utf-8", "ignore")
    print(found)

# ref. https://feneshi.co/ctf4b2021writeup/#be_angry