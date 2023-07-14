/** @typedef {import('./abstractStatements').StatementBase} StatementBase */

class StatementMixin {
  /**
   *
   * @param {RegExp} re
   * @param {string} line
   */
  constructor(re, line) {
    this.re = re;
    this.line = line;

    const parts = re.exec(line);
    if (parts === null || line.trimStart() != parts[0].trimStart()) {
      throw Error("Statement didn't match");
    }

    this.parts = parts;
    this.whitespacePrefix = line.substring(0, this.parts.index);
  }

  is_condition() {
    return false;
  }

  is_loop() {
    return false;
  }

  is_block_start() {
    return false;
  }

  is_block_end() {
    return false;
  }
}

/**
 * @param {string} strNumber
 * @returns {Number}
 */
function StringToInt(strNumber) {
  return JSON.parse(strNumber);
}

/**
 * @class
 * @implements {StatementBase}
 */
export class CheckFileEofBase extends StatementMixin {
  /** @param {string} line */
  constructor(line) {
    super(/IS ([a-zA-Z0-9.\-_]+) EMPTY ([a-zA-Z_]+[a-zA-Z0-9_]*) TELL ME PLS PLS PLS/, line);
    this.streamName = this.parts[1];
    this.varName = this.parts[2];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class CheckStdinEofBase extends StatementMixin {
  /** @param {string} line */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) HAVE YOU SEEN THIS/, line);
    this.varName = this.parts[1];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class CommentBase extends StatementMixin {
  /** @param {string} line */
  constructor(line) {
    super(/^.*$/, line);
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class ConditionBase extends StatementMixin {
  /** @param {string} line */
  constructor(line) {
    super(/IF ITS NOT ([a-zA-Z_]+[a-zA-Z0-9_]*) THEN VOTE ME/, line);
    this.varName = this.parts[1];
  }

  is_condition() {
    return true;
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class DecrementBase extends StatementMixin {
  /** @param {string} line */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) GOES DOWN( BY [0-9]+)?/, line);
    this.varName = this.parts[1];

    if (this.parts[2]) {
      this.byPresent = true;
      this.value = StringToInt(this.parts[2].slice(3));
    } else {
      this.byPresent = false;
      this.value = 1;
    }
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class DeleteFileBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/GAME ([a-zA-Z0-9.\-_]+) HAS FINISHED/, line);
    this.streamName = this.parts[1];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class EndBlockBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/ENDBLOCKUS/, line);
  }

  is_block_end() {
    return true;
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class ExitBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) WAS THE IMPOSTOR/, line);
    this.varName = this.parts[1];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class IncrementBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) GOES UP( BY [0-9]+)?/, line);

    this.varName = this.parts[1];

    if (this.parts[2]) {
      this.byPresent = true;
      this.value = StringToInt(this.parts[2].slice(3));
    } else {
      this.byPresent = false;
      this.value = 1;
    }
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class InputBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) WHO ARE YOU/, line);
    this.varName = this.parts[1];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class LoopBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/WHILE ITS NOT ([a-zA-Z_]+[a-zA-Z0-9_]*) VOTE ME/, line);
    this.varName = this.parts[1];
  }

  is_loop() {
    return true;
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class PrintBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) CAN VOUCH GO AND TELL THEM COME ON/, line);
    this.varName = this.parts[1];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class RandomBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/IDK WHAT ([a-zA-Z_]+[a-zA-Z0-9_]*) IS BUT ITS BETWEEN ([0-9]+) AND ([0-9]+)/, line);
    this.varName = this.parts[1];
    this.min = StringToInt(this.parts[2]);
    this.max = StringToInt(this.parts[3]);
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class ReadFileBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) HAS LEFT THE ([a-zA-Z0-9.\-_]+)/, line);
    this.varName = this.parts[1];
    this.streamName = this.parts[2];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class StartBlockBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/BLOCKUS/, line);
  }

  is_block_start() {
    return true;
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class ValueAssignmentBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/GUYS I CAN VOUCH ([a-zA-Z_]+[a-zA-Z0-9_]*) IS ([0-9]+)/, line);
    this.varName = this.parts[1];
    this.value = StringToInt(this.parts[2]);
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class VariableAssignmentBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) IS JUST LIKE ([a-zA-Z_]+[a-zA-Z0-9_]*)/, line);
    this.writeToVarName = this.parts[1];
    this.readFromVarName = this.parts[2];
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class WriteFileBase extends StatementMixin {
  /**
   * @param {string} line
   */
  constructor(line) {
    super(/([a-zA-Z_]+[a-zA-Z0-9_]*) HAS JOINED THE ([a-zA-Z0-9.\-_]+)/, line);
    this.varName = this.parts[1];
    this.streamName = this.parts[2];
  }
}
