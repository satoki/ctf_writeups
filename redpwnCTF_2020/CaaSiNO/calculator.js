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
