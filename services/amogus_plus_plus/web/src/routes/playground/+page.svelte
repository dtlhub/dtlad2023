<script>
  import { enhance } from '$app/forms';

  /** @type {import('./$types').PageData} */
  export let data;
</script>

<h1>CHOOSE WORKSPACE TO WORK IN</h1>

<ul>
  {#each data.workspaces as workspace}
    <li>
      <a href="/workspace/{workspace.id}" title={workspace.description}>{workspace.name}</a>
      <form method="POST" action="?/deleteWorkspace" use:enhance>
        <input hidden name="id" value={workspace.id} />
        <button>DELETE</button>
      </form>
    </li>
  {/each}

  <form method="POST" action="?/createWorkspace" use:enhance>
    <input
      name="name"
      type="text"
      size="30"
      maxlength="30"
      placeholder="NEW WORKSPACE NAME"
      required
    />
    <textarea name="description" placeholder="NEW WORKSPACE DESCRIPTION" rows="3" />
    <button>CREATE NEW WORKSPACE</button>
  </form>
</ul>

<style lang="scss">
  h1 {
    font-size: 2em;
    color: var(--white);
    margin-bottom: 1em;
  }

  ul {
    li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1em;

      a {
        text-decoration: none;
        color: var(--white);
        font-size: 1.5em;

        &:hover {
          color: var(--cyan);
        }
      }

      button {
        background-color: var(--red);
        outline: none;
        border: none;
        border-radius: 0.2em;
        font-size: 0.8em;

        &:hover {
          cursor: pointer;
          opacity: 0.8;
        }
      }
    }

    & > form {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: stretch;
      gap: 0.3em;
      margin-top: 1em;

      textarea,
      input {
        background-color: transparent;
        outline: none;
        color: var(--white);
        border: 2px solid var(--white);
        border-radius: 0.2em;
        padding: 0.1em;
        font-family: inherit;
        font-size: 0.8em;

        &:hover {
          border-color: var(--cyan);
        }

        &:focus {
          color: var(--cyan);
          border-color: var(--cyan);
        }
      }

      button {
        font-size: 0.8em;
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
</style>
