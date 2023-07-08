/**
 * @param {string} line
 * @param {any[]} statements
 * @param {DefaultStatement} DefaultStatement
 * @returns {any}
 */
export function getStatement(line, statements, DefaultStatement) {
  for (const Statement of statements) {
    try {
      return new Statement(line);
    } catch (err) {
      /* Line does not match statement */
    }
  }

  // If no other statements match
  return new DefaultStatement(line);
}
