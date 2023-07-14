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

      border: 2px solid var(--white);
      border-radius: 1em;

      font-family: inherit;
      font-size: 1em;
      color: color-mix(in srgb, var(--white), var(--surface));
    `
  };

  let editorContent = '';
  let stdin = '';
  let stdout = '';

  /** @type {string | null} */
  let activeFile = null;

  async function updateActiveFileContents() {
    if (activeFile === null) {
      editorContent = '';
      return;
    }

    const response = await fetch(`/workspace/${data.id}/${activeFile}`);
    editorContent = await response.json();
  }

  async function saveActiveFile() {
    if (activeFile === null) {
      return;
    }

    await fetch(`/workspace/${data.id}/${activeFile}`, {
      method: 'PUT',
      body: JSON.stringify({ filename: activeFile, content: editorContent })
    });
  }

  async function executeActiveFile() {
    if (activeFile === null) {
      return;
    }

    await saveActiveFile();

    const response = await fetch(`/workspace/${data.id}/${activeFile}`, {
      method: 'POST',
      body: JSON.stringify({ filename: activeFile, stdin })
    });

    const jsonData = await response.json();
    if (jsonData.errorMsg) {
      alert(jsonData.errorMsg);
    } else {
      data.files = jsonData.files;
      stdout = jsonData.stdout;
    }
  }

  /** @param {Event} event */
  async function onFileClick(event) {
    // @ts-ignore
    const newActiveFile = event.target.innerText;
    await saveActiveFile();
    activeFile = newActiveFile;
    await updateActiveFileContents();
  }

  onMount(async () => {
    if (data.files.length !== 0) {
      activeFile = data.files[0];
      await updateActiveFileContents();
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
            <form on:submit={saveActiveFile}>
              <button class="save">SAVE</button>
            </form>
          {/if}
          <form
            method="POST"
            action="?/deleteFile"
            use:enhance={() => {
              return async ({ result }) => {
                if (result.type === 'success') {
                  data.files = result.data;
                  if (!data.files.includes(activeFile)) {
                    activeFile = null;
                    updateActiveFileContents();
                  }
                }
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
          if (result.type === 'success') {
            data.files = result.data;
          }
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
      <svelte:component this={CodeJar} bind:value={editorContent} {...codejarConfig} />
    {:else}
      <p>Editor is loading</p>
      <p>You must have JavaScript enabled</p>
    {/if}
  </section>

  <section id="interactive">
    <section>
      <h3>STDIN</h3>
      <textarea id="stdin" bind:value={stdin} />
    </section>
    <section>
      <h3>STDOUT</h3>
      <pre id="stdout">{stdout}</pre>
    </section>

    <form on:submit={executeActiveFile}>
      <button>RUN</button>
    </form>
  </section>
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

    #interactive {
      overflow: auto;
      text-align: center;

      section {
        margin-bottom: 1em;

        h3 {
          margin-bottom: 0.5em;
        }
      }

      textarea,
      pre {
        width: 100%;
        height: 6em;
        resize: none;
        overflow: auto;
        padding: 0.2em 0.4em;

        box-sizing: border-box;
        background-color: var(--surface);
        border: 2px solid var(--white);
        outline: none;
        border-radius: 0.4em;

        color: var(--white);
        font-family: inherit;
        font-size: 1em;
        text-align: left;
      }

      button {
        background-color: var(--lime);
        border: none;
        border-radius: 0.4em;
        outline: none;
        font-size: 0.8em;
        padding: 0.2em 2em;

        &:hover {
          opacity: 0.8;
          cursor: pointer;
        }
      }
    }

    h3 {
      text-align: center;
      font-size: 1.2em;
      color: var(--white);
    }
  }
</style>
