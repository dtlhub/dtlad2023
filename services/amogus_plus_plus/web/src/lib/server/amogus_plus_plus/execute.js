import { getStatement } from '$lib/amogus_plus_plus/common';
import {
  ExecutableComment,
  ExitError,
  executableMeaningfulStatements
} from './executableStatements';
import Runtime from './runtime';

const MAX_ITERATIONS = 1000;

/**
 * @param {string} code
 * @param {string} workspaceId
 * @param {string} stdin
 * @returns {string} stdout
 */
export function execute(code, stdin, workspaceId) {
  const runtime = new Runtime(stdin, workspaceId);

  /** @type {import('./executableStatements').ExecutableStatement[]} */
  const lines = code
    .split('\n')
    .map((line) => getStatement(line, executableMeaningfulStatements, ExecutableComment));
  let index = 0;
  let iterations = 0;
  /** @type {import('./executableStatements').ExecutableStatement} */
  let currentLine;

  const nextLine = () => {
    if (index + 1 === lines.length) {
      throw new Error(`Expected statement after line ${index + 1}`);
    }
    return lines[index + 1];
  };

  const goToBlockEnd = () => {
    let blockDepth = 1;
    let i = index + 2;
    while (blockDepth != 0) {
      if (i >= lines.length) {
        throw new Error(`Unmached blockus at line ${index + 1}`);
      }
      if (lines[i].is_block_start()) ++blockDepth;
      if (lines[i].is_block_end()) --blockDepth;
      i += 1;
    }
    return i - 1;
  };

  const handleCondition = () => {
    // @ts-ignore
    if (!currentLine.execute(runtime)) {
      if (nextLine().is_block_start()) {
        index = goToBlockEnd();
      } else {
        ++index;
      }
    }
  };

  const handleLoop = () => {
    if (nextLine().is_block_start()) {
      handleCondition();
    } else {
      // @ts-ignore
      if (currentLine.execute(runtime)) {
        nextLine().execute(runtime);
        index -= 1;
      } else {
        index += 1;
      }
    }
  };

  const handleBlockStart = () => {
    runtime.jumpStack.push(index);
  };

  const handleBlockEnd = () => {
    if (runtime.jumpStack.length === 0) {
      throw new Error(`Unmached endblockus at line ${index}`);
    }
    const blockStart = runtime.jumpStack.pop();
    if (lines[blockStart - 1].is_loop()) {
      index = blockStart - 2;
    }
  };

  try {
    while (index !== lines.length && iterations++ < MAX_ITERATIONS) {
      currentLine = lines[index];

      if (currentLine.is_condition()) {
        handleCondition();
      } else if (currentLine.is_loop()) {
        handleLoop();
      } else if (currentLine.is_block_start()) {
        handleBlockStart();
      } else if (currentLine.is_block_end()) {
        handleBlockEnd();
      } else {
        currentLine.execute(runtime);
      }

      ++index;
    }

    if (iterations >= MAX_ITERATIONS) {
      throw new Error('Reached iteration limit');
    }
  } catch (err) {
    if (err instanceof ExitError) {
      return err.stdout;
    } else {
      throw err;
    }
  }

  return runtime.Stdout;
}
