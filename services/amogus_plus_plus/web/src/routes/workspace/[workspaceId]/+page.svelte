<script>
  import { applyAction, enhance } from '$app/forms';
  import { highlight } from '$lib/amogus_plus_plus/highlightableStatements';
  import { onMount } from 'svelte';

  /** @type {import('./$types').PageData} */
  export let data;

  /** @type {any} */
  let CodeJar;
  onMount(async () => {
    ({ CodeJar } = await import('@novacbn/svelte-codejar'));
  });

  const codejarConfig = {
    highlight: highlight,
    indentOn: /BLOCKUS$/,
    addClosing: false,
    style: `
      width: 100%;
      height: 100%;
      box-sizing: border-box;
      padding: 0.4em 0.6em;

      background-color: var(--surface);

      border: 1px solid var(--white);
      border-radius: 1em;

      font-family: inherit;
      font-size: 1em;
      color: color-mix(in srgb, var(--white), var(--surface));
    `
  };

  let value = '';

  /** @type {string | null} */
  let activeFile = null;

  function updateFileContents() {
    if (activeFile === null) {
      value = '';
      return;
    }

    fetch(`/workspace/${data.id}/${activeFile}`)
      .then((response) => response.json())
      .then((data) => (value = data));
  }

  function saveData() {
    if (activeFile === null) {
      return;
    }

    fetch(`/workspace/${data.id}/${activeFile}`, {
      method: 'POST',
      body: JSON.stringify({ filename: activeFile, content: value })
    });
  }

  /** @param {Event} event */
  function onFileClick(event) {
    // @ts-ignore
    const newActiveFile = event.target.innerText;
    saveData();
    activeFile = newActiveFile;
    updateFileContents();
  }

  onMount(() => {
    if (data.files.length !== 0) {
      updateFileContents(data.files[0]);
    }
  });
</script>

<h1>{data.name}</h1>

<div id="workspace-grid">
  <section id="files">
    <h3>FILES</h3>

    {#each data.files as file}
      <div class="file">
        <!-- svelte-ignore a11y-missing-attribute -->
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <a on:click={onFileClick} class={file === activeFile ? 'active' : ''}>{file}</a>

        <div class="file-buttons">
          {#if file === activeFile}
            <form on:submit={saveData}>
              <button class="save">SAVE</button>
            </form>
          {/if}
          <form
            method="POST"
            action="?/deleteFile"
            use:enhance={() => {
              return async ({ result }) => {
                data.files = result.data;
                await applyAction(result);
              };
            }}
          >
            <input hidden name="filename" value={file} />
            <button class="delete">DEL</button>
          </form>
        </div>
      </div>
    {/each}

    <form
      method="POST"
      action="?/createFile"
      use:enhance={() => {
        return async ({ result }) => {
          data.files = result.data;
          await applyAction(result);
        };
      }}
    >
      <input name="filename" type="text" placeholder="New file name" />
      <button>CREATE</button>
    </form>
  </section>

  <section id="editor">
    {#if CodeJar}
      <svelte:component
        this={CodeJar}
        bind:value
        on:change={() => console.log(value)}
        {...codejarConfig}
      />
    {:else}
      <p>Editor is loading</p>
      <p>You must have JavaScript enabled</p>
    {/if}
  </section>

  <section id="extra" />
</div>

<style lang="scss">
  h1 {
    font-size: 2em;
    text-align: center;
    color: var(--white);
    margin: -0.5em 0 1em 0;
  }

  p {
    text-align: center;
    color: var(--white);
  }

  #workspace-grid {
    display: grid;
    grid-template-columns: 2fr 6fr 3fr;
    gap: 1em;
    width: 80vw;
    max-width: 80vw;
    height: 60vh;
    max-height: 60vh;
    margin: -0.8em;
    justify-items: stretch;

    #files {
      overflow: auto;

      .file {
        display: flex;
        justify-content: space-between;
        align-items: center;
        justify-items: stretch;
        margin-bottom: 0.1em;

        a {
          text-decoration: none;
          color: var(--white);
          font-size: 0.8em;

          &.active {
            margin-left: 0.5em;
            text-decoration: underline;
          }

          &:hover {
            cursor: pointer;
            color: var(--cyan);
          }
        }

        .file-buttons {
          display: flex;
          flex-direction: row;
          gap: 0.2em;

          form {
            display: flex;
            align-items: center;

            button {
              &.delete {
                background-color: var(--red);
              }
              &.save {
                background-color: var(--cyan);
              }
              outline: none;
              border: none;
              border-radius: 0.2em;
              font-size: 0.6em;

              &:hover {
                cursor: pointer;
                opacity: 0.8;
              }
            }
          }
        }
      }

      & > form {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: stretch;
        gap: 0.2em;
        margin-top: 1em;

        input {
          background-color: transparent;
          outline: none;
          color: var(--white);
          border: 2px solid var(--white);
          border-radius: 0.2em;
          font-family: inherit;
          font-size: 0.8em;
          text-align: center;

          &:hover {
            border-color: var(--cyan);
          }

          &:focus {
            color: var(--cyan);
            border-color: var(--cyan);
          }
        }

        button {
          font-size: 0.6em;
          background-color: var(--cyan);
          border: none;
          outline: none;
          border-radius: 0.2em;

          &:hover {
            cursor: pointer;
            opacity: 0.8;
          }
        }
      }
    }

    #editor {
      justify-items: stretch;
      overflow-y: hidden;
      overflow-x: auto;
    }

    #extra {
      border: 1px solid cyan;
    }

    h3 {
      text-align: center;
      font-size: 1.2em;
      color: var(--white);
    }
  }
</style>
