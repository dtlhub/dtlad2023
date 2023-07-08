/** @typedef {import('./abstractStatements').StatementBase} StatementBase */

class StatementMixin {
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
 * @class
 * @implements {StatementBase}
 */
export class CommentBase extends StatementMixin {
  /** @param {string} line */
  constructor(line) {
    super();

    this.line = line;
  }
}

/**
 * @class
 * @implements {StatementBase}
 */
export class ConditionBase extends StatementMixin {
  /** @param {string} line */
  constructor(line) {
    super();

    const parts = /IF ITS NOT ([a-zA-Z_]+[a-zA-Z0-9_]*) THEN VOTE ME/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) GOES DOWN( BY [0-9]+)?/.exec(line);

    if (parts === null) {
      throw Error("Statement didn't match");
    }

    this.varName = parts[1];

    if (parts[2]) {
      this.byPresent = true;
      this.value = Number.parseInt(parts[2].slice(3));
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
    super();

    const parts = /GAME ([a-zA-Z0-9.-_]+) HAS FINISHED/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.streamName = parts[1];
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
    super();

    if (line != 'ENDBLOCKUS') {
      throw Error("Statement didn'd match");
    }
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) WAS THE IMPOSTOR/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) GOES UP( BY [0-9]+)?/.exec(line);

    if (parts === null) {
      throw Error("Statement didn't match");
    }

    this.varName = parts[1];

    if (parts[2]) {
      this.byPresent = true;
      this.value = Number.parseInt(parts[2].slice(3));
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) WHO ARE YOU/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
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
    super();

    const parts = /WHILE ITS NOT ([a-zA-Z_]+[a-zA-Z0-9_]*) VOTE ME/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) CAN VOUCH GO AND TELL THEM COME ON/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
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
    super();

    const parts =
      /IDK WHAT ([a-zA-Z_]+[a-zA-Z0-9_]*) IS BUT ITS BETWEEN ([0-9]+) AND ([0-9]+)/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
    this.min = Number.parseInt(parts[2]);
    this.max = Number.parseInt(parts[3]);
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) HAS LEFT THE ([a-zA-Z0-9.-_]+)/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
    this.streamName = parts[2];
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
    super();

    if (line != 'BLOCKUS') {
      throw Error("Statement didn'd match");
    }
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
    super();

    const parts = /GUYS I CAN VOUCH ([a-zA-Z_]+[a-zA-Z0-9_]*) IS ([0-9]+)/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
    this.value = parts[2];
    console.log();
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) IS JUST LIKE ([a-zA-Z_]+[a-zA-Z0-9_]*)/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.writeToVarName = parts[1];
    this.readFromVarName = parts[2];
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
    super();

    const parts = /([a-zA-Z_]+[a-zA-Z0-9_]*) HAS JOINED THE ([a-zA-Z0-9.-_]+)/.exec(line);

    if (parts === null) {
      throw Error("Statement didn'd match");
    }

    this.varName = parts[1];
    this.streamName = parts[2];
  }
}
