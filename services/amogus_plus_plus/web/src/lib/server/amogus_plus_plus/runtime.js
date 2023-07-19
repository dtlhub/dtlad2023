import { fileContents } from '../workspaceUtils';

class FileReader {
  /** @param {string} content */
  constructor(content) {
    this._content = content;
    this._pos = 0;
  }

  /** @returns {Number} */
  next() {
    if (this._pos >= this._content.length) {
      throw new Error('Unable to read next character');
    }
    return this._content.charCodeAt(this._pos++);
  }

  reachedEof() {
    return this._pos >= this._content.length;
  }
}

/**
 * @param {any} target
 * @param {any} source
 */
function merge(target, source) {
  for (const key in source) {
    if (typeof target[key] === 'object' && typeof source[key] === 'object') {
      merge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
}

export default class Runtime {
  /**
   * @param {string} stdin
   * @param {string} workspaceId
   */
  constructor(stdin, workspaceId) {
    this.workspaceId = workspaceId;

    this._stdin = new FileReader(stdin);
    this._stdout = '';

    this._filereaders = {};
    this._storage = {};

    this.jumpStack = [];
  }

  /** @param {string} filename */
  fileReader(filename) {
    if (!(filename in this._filereaders)) {
      const content = fileContents(this.workspaceId, filename).toString();
      // @ts-ignore
      this._filereaders[filename] = new FileReader(content);
    }
    // @ts-ignore
    return this._filereaders[filename];
  }

  /** @param {string} key */
  getFromStorage(key) {
    if (!(key in this._storage)) {
      throw new Error(`Variable ${key} is not defined`);
    }
    // @ts-ignore
    return this._storage[key];
  }

  /**
   * @param {string} key
   * @param {any} value
   */
  addToStorage(key, value) {
    if (typeof value !== 'object') {
      // @ts-ignore
      this._storage[key] = value;
    } else {
      if (!(key in this._storage)) {
        // @ts-ignore
        this._storage[key] = new Object();
      }
      // @ts-ignore
      merge(this._storage[key], value);
    }
  }

  get Stdout() {
    return this._stdout;
  }

  /** @param {Number} char */
  writeToStdout(char) {
    this._stdout += String.fromCharCode(char);
  }

  readFromStdin() {
    return this._stdin.next();
  }

  hasStdinReachedEof() {
    return this._stdin.reachedEof();
  }
}
