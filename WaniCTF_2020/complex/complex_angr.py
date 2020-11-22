import angr

p = angr.Project("./complex")
state = p.factory.entry_state()
sim = p.factory.simulation_manager(state)
sim.explore(find=(0x400000+0x1cad,), avoid=(0x400000+0x1c8d,))
if len(sim.found) > 0:
    print(sim.found[0].posix.dumps(0))