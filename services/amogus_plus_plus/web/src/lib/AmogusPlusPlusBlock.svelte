<script>
  import { highlight } from './amogus_plus_plus/highlightableStatements';

  /** @type {string} */
  let value;
  /** @type {string} */
  let highlightedValue = '';

  function onChange() {
    highlightedValue = highlight(value);
  }
</script>

<textarea bind:value on:change={onChange} on:input={onChange} on:paste={onChange} rows="10" />

<code
  ><pre>
{@html highlightedValue}
</pre></code
>

<style>
  textarea {
    width: 60vw;
    padding: 0.2em 0.4em;

    background-color: var(--surface);

    border: 1px solid var(--white);
    border-radius: 1em;

    font-family: inherit;
    font-size: 1em;
    color: color-mix(in srgb, var(--white), var(--surface));
  }
</style>
