/** @typedef {import('../../amogus_plus_plus/abstractStatements').ExecutableStatement} ExecutableStatement */

import {
  CheckFileEofBase,
  CheckStdinEofBase,
  CommentBase,
  ConditionBase,
  DecrementBase,
  DeleteFileBase,
  EndBlockBase,
  ExitBase,
  IncrementBase,
  InputBase,
  LoopBase,
  PrintBase,
  RandomBase,
  ReadFileBase,
  StartBlockBase,
  ValueAssignmentBase,
  VariableAssignmentBase,
  WriteFileBase
} from '$lib/amogus_plus_plus/statementsBases';
import { appendToFile, removeFile } from '../workspaceUtils';

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableCheckFileEof extends CheckFileEofBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const file = runtime.fileReader(this.streamName);
    runtime.addToStorage(this.varName, file.reachedEof() ? 0 : 1);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableCheckStdinEof extends CheckStdinEofBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    runtime.addToStorage(this.varName, runtime.hasStdinReachedEof() ? 0 : 1);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableComment extends CommentBase {
  /** @param {import("./runtime").default} runtime */
  // eslint-disable-next-line no-unused-vars
  execute(runtime) {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableCondition extends ConditionBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const value = runtime.getFromStorage(this.varName);
    return value !== 0;
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableDecrement extends DecrementBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const currentValue = runtime.getFromStorage(this.varName);
    runtime.addToStorage(this.varName, (currentValue - this.value + 256) % 256);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableDeleteFile extends DeleteFileBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    removeFile(runtime.workspaceId, this.streamName);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableEndBlock extends EndBlockBase {
  /** @param {import("./runtime").default} runtime */
  // eslint-disable-next-line no-unused-vars
  execute(runtime) {}
}

export class ExitError extends Error {
  /** @param {string} stdout */
  constructor(stdout) {
    super();
    this.stdout = stdout;
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableExit extends ExitBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const value = runtime.getFromStorage(this.varName);
    if (value !== 0) {
      throw new ExitError(runtime.Stdout);
    }
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableIncrement extends IncrementBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const currentValue = runtime.getFromStorage(this.varName);
    runtime.addToStorage(this.varName, (currentValue + this.value) % 256);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableInput extends InputBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const value = runtime.readFromStdin();
    runtime.addToStorage(this.varName, value);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableLoop extends LoopBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const value = runtime.getFromStorage(this.varName);
    return value !== 0;
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutablePrint extends PrintBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const value = runtime.getFromStorage(this.varName);
    runtime.writeToStdout(value);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableRandom extends RandomBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    if (this.min > this.max) {
      throw new Error(`Maximum value (${this.max}) can't be less than minimum (${this.min})`);
    }
    const value = Math.floor(Math.random() * (this.max + 1 - this.min)) + this.min;
    runtime.addToStorage(this.varName, value);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableReadFile extends ReadFileBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const char = runtime.fileReader(this.streamName).next();
    runtime.addToStorage(this.varName, char);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableStartBlock extends StartBlockBase {
  /** @param {import("./runtime").default} runtime */
  // eslint-disable-next-line no-unused-vars
  execute(runtime) {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableValueAssignment extends ValueAssignmentBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    runtime.addToStorage(this.varName, this.value);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableVariableAssignment extends VariableAssignmentBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    const value = runtime.getFromStorage(this.readFromVarName);
    runtime.addToStorage(this.writeToVarName, value);
  }
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableWriteFile extends WriteFileBase {
  /** @param {import("./runtime").default} runtime */
  execute(runtime) {
    // @ts-ignore
    const char = String.fromCharCode([runtime.getFromStorage(this.varName)]);
    appendToFile(runtime.workspaceId, this.streamName, char);
  }
}

export const executableMeaningfulStatements = [
  ExecutableCheckFileEof,
  ExecutableCheckStdinEof,
  ExecutableCondition,
  ExecutableDecrement,
  ExecutableDeleteFile,
  ExecutableEndBlock,
  ExecutableExit,
  ExecutableIncrement,
  ExecutableInput,
  ExecutableLoop,
  ExecutablePrint,
  ExecutableRandom,
  ExecutableReadFile,
  ExecutableStartBlock,
  ExecutableValueAssignment,
  ExecutableVariableAssignment,
  ExecutableWriteFile
];
