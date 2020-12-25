import angr

p = angr.Project("./first_asm")
state = p.factory.entry_state()
sim = p.factory.simulation_manager(state)
sim.explore(find=(0x400000+0x126b,), avoid=(0x400000+0x1279,))
if len(sim.found) > 0:
    print(sim.found[0].posix.dumps(0))