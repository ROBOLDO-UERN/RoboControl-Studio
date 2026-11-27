import { spawn } from 'node:child_process';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const pythonCommand = process.env.PYTHON || 'py';

const serverProcess = spawn(pythonCommand, ['server.py'], {
  cwd: __dirname,
  stdio: 'inherit',
  shell: false,
});

serverProcess.on('exit', (code, signal) => {
  if (signal) {
    console.error(`Servidor Piper finalizado por sinal: ${signal}`);
    process.exit(1);
  }
  process.exit(code ?? 0);
});

serverProcess.on('error', (error) => {
  console.error('Erro ao iniciar o servidor Python do Piper:', error.message);
  process.exit(1);
});