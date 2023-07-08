/** @typedef {import('../../amogus_plus_plus/abstractStatements').ExecutableStatement} ExecutableStatement */

import { getStatement } from '$lib/amogus_plus_plus/common';
import {
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

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableComment extends CommentBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableCondition extends ConditionBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableDecrement extends DecrementBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableDeleteFile extends DeleteFileBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableEndBlock extends EndBlockBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableExit extends ExitBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableIncrement extends IncrementBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableInput extends InputBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableLoop extends LoopBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutablePrint extends PrintBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableRandom extends RandomBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableReadFile extends ReadFileBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableStartBlock extends StartBlockBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableValueAssignment extends ValueAssignmentBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableVariableAssignment extends VariableAssignmentBase {
  execute() {}
}

/**
 * @class
 * @implements {ExecutableStatement}
 */
export class ExecutableWriteFile extends WriteFileBase {
  execute() {}
}

const executableMeaningfulStatements = [
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

/**
 * @param {string} text
 * @returns {string}
 */
export function execute(text) {
  return text
    .split('\n')
    .map((line) =>
      getStatement(line, executableMeaningfulStatements, ExecutableComment).highlight()
    )
    .join('\n');
}
