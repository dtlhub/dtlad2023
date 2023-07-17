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
      throw new Error("Statement didn't match");
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
    super(/IS ([^\s]+) EMPTY ([^\s]+) TELL ME PLS PLS PLS/, line);
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
    super(/([^\s]+) HAVE YOU SEEN THIS/, line);
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
    super(/IF ITS NOT ([^\s]+) THEN VOTE ME/, line);
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
    super(/([^\s]+) GOES DOWN( BY [^\s]+)?/, line);
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
    super(/GAME ([^\s]+) HAS FINISHED/, line);
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
    super(/([^\s]+) WAS THE IMPOSTOR/, line);
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
    super(/([^\s]+) GOES UP( BY [^\s]+)?/, line);

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
    super(/([^\s]+) WHO ARE YOU/, line);
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
    super(/WHILE ITS NOT ([^\s]+) VOTE ME/, line);
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
    super(/([^\s]+) CAN VOUCH GO AND TELL THEM COME ON/, line);
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
    super(/IDK WHAT ([^\s]+) IS BUT ITS BETWEEN ([^\s]+) AND ([^\s]+)/, line);
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
    super(/([^\s]+) HAS LEFT THE ([^\s]+)/, line);
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
    super(/GUYS I CAN VOUCH ([^\s]+) IS ([^\s]+)/, line);
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
    super(/([^\s]+) IS JUST LIKE ([^\s]+)/, line);
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
    super(/([^\s]+) HAS JOINED THE ([^\s]+)/, line);
    this.varName = this.parts[1];
    this.streamName = this.parts[2];
  }
}
