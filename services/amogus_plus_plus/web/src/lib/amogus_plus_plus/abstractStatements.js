/* eslint-disable constructor-super */
// @ts-nocheck
/* eslint-disable no-unused-vars */

/** @interface  */
export class StatementBase {
  /** @param {string} line */
  constructor(line) {}

  /** @returns {boolean} */
  is_condition() {}

  /** @returns {boolean} */
  is_loop() {}

  /** @returns {boolean} */
  is_block_start() {}

  /** @returns {boolean} */
  is_block_end() {}
}

/** @interface */
export class HighlightableStatement extends StatementBase {
  /** @param {string} line */
  constructor(line) {}

  /** @returns {string} */
  highlight() {}
}

/** @interface */
export class ExecutableStatement extends StatementBase {
  /** @param {string} line */
  constructor(line) {}

  execute() {}
}
