import angr

p = angr.Project("./hotel_key_puzzle")
state = p.factory.entry_state()
sim = p.factory.simulation_manager(state)
sim.explore(find=(0x400000+0x22ba,), avoid=(0x400000+0x22c8,))
if len(sim.found) > 0:
    print(sim.found[0].posix.dumps(0))