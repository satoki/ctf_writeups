import angr

p = angr.Project("./yakisoba")
state = p.factory.entry_state()
sim = p.factory.simulation_manager(state)
sim.explore(find=(0x400000+0x6d2,), avoid=(0x400000+0x6f7,))
if len(sim.found) > 0:
    print(sim.found[0].posix.dumps(0))