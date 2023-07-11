<h1>Documentation</h1>

<h2>About</h2>

<p>
  <span class="lang"
    >AMONGUSISABIGSUSSYBAKAHAHAHAHAHATHISLANGUAGEISREALLYCOOLPLEASEUSEITMYLIFEDEPENDSONITORELSEPLSPLSPLSPLSPLSPLSPLSkahyghdfhm++</span
  >
  or, for short, <span class="lang">ඞ++</span> (read as "amogus plus plus") is an interpreted
  programming language. It is a superset of
  <a
    href="https://esolangs.org/wiki/AMONGUSISABIGSUSSYBAKAHAHAHAHAHATHISLANGUAGEISREALLYCOOLPLEASEUSEITMYLIFEDEPENDSONITORELSEPLSPLSPLSPLSPLSPLSPLSkahyghdfhm"
    >AMONGUSISABIGSUSSYBAKAHAHAHAHAHATHISLANGUAGEISREALLYCOOLPLEASEUSEITMYLIFEDEPENDSONITORELSEPLSPLSPLSPLSPLSPLSPLSkahyghdfhm</a
  >, created by SpaceBytes in 2022, introducing couple of new features, such as blocks, loops and
  file I/O.
</p>

<h2>General information</h2>
<ul>
  <li>
    <span class="lang">ඞ++</span> is interpreted line-by-line. That means if a line results in any errors,
    all previous lines still will be executed before throwing a error.
  </li>
  <li>
    <span class="lang">ඞ++</span> variables and statements are case-sensetive. All statements MUST be
    written in yelling uppercase (not applied to variable and stream names).
  </li>
  <li>
    <span class="lang">ඞ++</span> has two entities: variables and streams.
  </li>
  <li>
    Variables are integers that can contain any value between <span class="value">0</span> and
    <span class="value">255</span>. If any operation overflows the variable, it wraps around.
    There's also a special case, in which <span class="value">-1</span> can be assigned to variable,
    when reading from stream or stdin that reached EOF.
  </li>
  <li>
    Streams are strings, which represent filenames in local directory. Filenames must be matchable
    by <span class="stream">[A-Za-z0-9._-]+</span>. If stream has not been open yet, reading from it
    opens it and returns first byte of file (or <span class="value">-1</span>, if file is empty). If
    stream has already been open, reading from it just returns first unread byte from the file.
    Writing to a non-existing file will create that file on the filesystem. Simultaneuos reading and
    writing to the same file is prohibited.
  </li>
</ul>

<h2>Command reference</h2>

<p>Here's the list of all the commands, interpreted by <span class="lang">ඞ++</span>:</p>

<table>
  <thead>
    <th>Statemtent</th>
    <th>Description</th>
  </thead>
  <tbody>
    <!-- GUYS I CAN VOUCH [PLAYER] IS [VALUE] -->
    <tr>
      <td class="code"
        >GUYS I CAN VOUCH <span class="var">[PLAYER]</span> IS
        <span class="value">[VALUE]</span></td
      >
      <td
        >Sets variable <span class="var">[PLAYER]</span> to integer
        <span class="value">[VALUE]</span></td
      >
    </tr>

    <!-- [PLAYER] CAN VOUCH GO AND TELL THEM COME ON -->
    <tr>
      <td class="code"><span class="var">[PLAYER]</span> CAN VOUCH GO AND TELL THEM COME ON</td>
      <td
        >Prints ascii character of the id of the variable <span class="var">[PLAYER]</span>'s value
        to stdout</td
      >
    </tr>

    <!-- [PLAYER] IS JUST LIKE [SUSSYPLAYER] -->
    <tr>
      <td class="code"
        ><span class="var">[PLAYER]</span> IS JUST LIKE <span class="var">[SUSSYPLAYER]</span></td
      >
      <td
        >Sets <span class="var">[PLAYER]</span>'s value to that of
        <span class="var">[SUSSYPLAYER]</span></td
      >
    </tr>

    <!-- IF ITS NOT [PLAYER] THEN VOTE ME -->
    <tr>
      <td class="code">IF ITS NOT <span class="var">[PLAYER]</span> THEN VOTE ME</td>
      <td
        >If <span class="var">[PLAYER]</span>'s value is not <span class="value">0</span>, execute
        the next line, otherwise, skip it</td
      >
    </tr>

    <!-- [PLAYER] IS BETWEEN [MIN] AND [MAX] -->
    <tr>
      <td class="code"
        >IDK WHAT <span class="var">[PLAYER]</span> IS BUT ITS BETWEEN
        <span class="value">[MIN]</span>
        AND <span class="value">[MAX]</span></td
      >
      <td
        >Set <span class="var">[PLAYER]</span>'s value to a random integer between
        <span class="value">[MIN]</span>
        and <span class="value">[MAX]</span></td
      >
    </tr>

    <!-- [PLAYER] WAS THE IMPOSTOR -->
    <tr>
      <td class="code"><span class="var">[PLAYER]</span> WAS THE IMPOSTOR</td>
      <td
        >If <span class="var">[PLAYER]</span> is not <span class="value">0</span>, end the program
        at that line</td
      >
    </tr>

    <!-- [PLAYER] GOES UP (BY [VALUE]) -->
    <tr>
      <td class="code"
        ><span class="var">[PLAYER]</span> GOES UP
        <span class="optional">(BY <span class="value">[VALUE]</span>)</span></td
      >
      <td
        >Add <span class="value">[VALUE]</span> to <span class="var">[PLAYER]</span>. If
        <span class="optional">BY</span>
        block is not present, add <span class="value">1</span></td
      >
    </tr>

    <!-- [PLAYER] GOES DOWN (BY [VALUE]) -->
    <tr>
      <td class="code"
        ><span class="var">[PLAYER]</span> GOES DOWN
        <span class="optional">(BY <span class="value">[VALUE]</span>)</span></td
      >
      <td
        >Subtract <span class="value">[VALUE]</span> from <span class="var">[PLAYER]</span>. If
        <span class="optional">BY</span>
        block is not present, substract <span class="value">1</span></td
      >
    </tr>

    <!-- [PLAYER] WHO ARE YOU -->
    <tr>
      <td class="code"><span class="var">[PLAYER]</span> WHO ARE YOU</td>
      <td
        >Recieve a character as user input from stdin, and save it's ascii value at <span
          class="var">[PLAYER]</span
        >. If stdin is empty, sets <span class="var">[PLAYER]</span> to
        <span class="value">-1</span></td
      >
    </tr>

    <!-- WHILE ITS NOT [PLAYER] VOTE ME -->
    <tr>
      <td class="code">WHILE ITS NOT <span class="var">[PLAYER]</span> VOTE ME</td>
      <td
        >While <span class="var">[PLAYER]</span>'s value is not <span class="value">0</span>,
        execute the next line</td
      >
    </tr>

    <!-- [PLAYER] HAS LEFT THE [LOBBY] -->
    <tr>
      <td class="code"
        ><span class="var">[PLAYER]</span> HAS LEFT THE <span class="stream">[LOBBY]</span></td
      >
      <td
        >Read next character from file <span class="stream">[LOBBY]</span> and save it's ASCII value
        into <span class="var">[PLAYER]</span>. If reached EOF, writes
        <span class="value">-1</span></td
      >
    </tr>

    <!-- [PLAYER] HAS JOINED THE [LOBBY] -->
    <tr>
      <td class="code"
        ><span class="var">[PLAYER]</span> HAS JOINED THE <span class="stream">[LOBBY]</span></td
      >
      <td
        >Appends character <span class="var">[PLAYER]</span> to the file.
        <span class="stream">[LOBBY]</span>. If <span class="stream">[LOBBY]</span> does not exist, creates
        it with empty content</td
      >
    </tr>

    <!-- GAME [LOBBY] HAS FINISHED -->
    <tr>
      <td class="code">GAME <span class="stream">[LOBBY]</span> HAS FINISHED</td>
      <td>Remove file <span class="stream">[LOBBY]</span> from filesystem, if it exists</td>
    </tr>

    <!-- BLOCKUS -->
    <tr>
      <td class="code">BLOCKUS</td>
      <td
        >Marks the beginning of the code block. The whole block will be treated as a single line
      </td>
    </tr>

    <!-- ENDBLOCKUS -->
    <tr>
      <td class="code">ENDBLOCKUS</td>
      <td>Marks the end of the code block</td>
    </tr>
  </tbody>
</table>

<h2>Examples</h2>

<style lang="scss">
  * {
    color: var(--white);
  }

  h1 {
    font-size: 2em;
    margin-bottom: 1em;
    text-align: center;
  }

  h2 {
    font-size: 1.5em;
    margin-top: 0.5em;
    margin-bottom: 0.2em;
  }

  table {
    table-layout: fixed;
    margin-top: 1em;
  }

  ul {
    list-style-type: disc;
  }

  a {
    &:hover {
      color: var(--cyan);
    }
  }

  table,
  th,
  td {
    border: 1px solid var(--white);
  }

  th,
  td {
    padding: 0.2em 0.4em;
  }

  td {
    width: 50%;
    vertical-align: middle;

    &.code {
      text-align: center;
    }
  }

  .var {
    color: var(--cyan);
  }

  .lang,
  .value {
    color: var(--red);
  }

  .optional {
    color: var(--yellow);
  }

  .stream {
    color: var(--pink);
  }
</style>
