/** @typedef {import('./abstractStatements').HighlightableStatement} HighlightableStatement */

import { getStatement } from './common';
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
} from './statementsBases';

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableComment extends CommentBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: color-mix(in srgb, var(--white), var(--surface))">${this.line}</span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableCondition extends ConditionBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)">IF ITS NOT <span style="color: var(--cyan)">${this.varName}</span> THEN VOTE ME</span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableDecrement extends DecrementBase {
  highlight() {
    const base = `<span style="color: var(--cyan)">${this.varName}</span> GOES DOWN`;
    let by = '';
    if (this.byPresent) {
      by = `<span style="color: var(--yellow)">BY</span> <span style="color: var(--red)">${this.value}</span>`;
    }
    return this.whitespacePrefix + `<span style="color: var(--white)">${base} ${by}</span>`;
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableDeleteFile extends DeleteFileBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)">GAME <span style="color: var(--pink)">${this.streamName}</span> HAS FINISHED</span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableEndBlock extends EndBlockBase {
  highlight() {
    return '<span style="color: var(--white)">ENDBLOCKUS</span>';
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableExit extends ExitBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)"><span style="color: var(--cyan)">${this.varName}</span> WAS THE IMPOSTOR</span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableIncrement extends IncrementBase {
  highlight() {
    const base = `<span style="color: var(--cyan)">${this.varName}</span> GOES UP`;
    let by = '';
    if (this.byPresent) {
      by = `<span style="color: var(--yellow)">BY</span> <span style="color: var(--red)">${this.value}</span>`;
    }
    return this.whitespacePrefix + `<span style="color: var(--white)">${base} ${by}</span>`;
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableInput extends InputBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)"><span style="color: var(--cyan)">${this.varName}</span> WHO ARE YOU</span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableLoop extends LoopBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)">WHILE ITS NOT <span style="color: var(--cyan)">${this.varName}</span> VOTE ME</span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightablePrint extends PrintBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)"><span style="color: var(--cyan)">${this.varName}</span> CAN VOUCH GO ON AND TELL THEM COME ON</span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableRandom extends RandomBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)">IDK WHAT <span style="color: var(--cyan)">${this.varName}</span> IS BUT ITS BETWEEN <span style="color: var(--red)">${this.min}</span> AND <span style="color: var(--red)">${this.max}</span></span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableReadFile extends ReadFileBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)"><span style="color: var(--cyan)">${this.varName}</span> HAS LEFT THE <span style="color: var(--pink)">${this.streamName}</span></span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableStartBlock extends StartBlockBase {
  highlight() {
    return '<span style="color: var(--white)">BLOCKUS</span>';
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableValueAssignment extends ValueAssignmentBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)">GUYS I CAN VOUCH <span style="color: var(--cyan)">${this.varName}</span> IS <span style="color: var(--red)">${this.value}</span></span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableVariableAssignment extends VariableAssignmentBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)"><span style="color: var(--cyan)">${this.writeToVarName}</span> IS JUST LIKE <span style="color: var(--cyan)">${this.readFromVarName}</span></span>`
    );
  }
}

/**
 * @class
 * @implements {HighlightableStatement}
 */
export class HighlightableWriteFile extends WriteFileBase {
  highlight() {
    return (
      this.whitespacePrefix +
      `<span style="color: var(--white)"><span style="color: var(--cyan)">${this.varName}</span> HAS JOINED THE <span style="color: var(--pink)">${this.streamName}</span></span>`
    );
  }
}

const highlightableMeaningfulStatements = [
  HighlightableCondition,
  HighlightableDecrement,
  HighlightableDeleteFile,
  HighlightableEndBlock,
  HighlightableExit,
  HighlightableIncrement,
  HighlightableInput,
  HighlightableLoop,
  HighlightablePrint,
  HighlightableRandom,
  HighlightableReadFile,
  HighlightableStartBlock,
  HighlightableValueAssignment,
  HighlightableVariableAssignment,
  HighlightableWriteFile
];

/**
 * @param {string} text
 * @returns {string}
 */
export function highlight(text) {
  return text
    .split('\n')
    .map((line) =>
      getStatement(line, highlightableMeaningfulStatements, HighlightableComment).highlight()
    )
    .join('\n');
}
