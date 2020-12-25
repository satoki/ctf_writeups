import angr

p = angr.Project("./dummy")
state = p.factory.entry_state()
sim = p.factory.simulation_manager(state)
sim.explore(find=(0x400000+0x7e209,), avoid=(0x400000+0x7e1fb,))
if len(sim.found) > 0:
    print(sim.found[0].posix.dumps(0))