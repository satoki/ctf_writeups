import angr

p = angr.Project("./chall")
state = p.factory.entry_state()
sim = p.factory.simulation_manager(state)
sim.explore(find=(0x400000+0x1321,), avoid=(0x400000+0x133b,))
if len(sim.found) > 0:
    print(sim.found[0].posix.dumps(0))