<script>
  import { enhance } from '$app/forms';
  import { currentUser } from '$lib/pocketbase';

  const workspaces = [
    { id: 0, name: 'aboba' },
    { id: 1, name: 'amogus' },
    { id: 2, name: 'something' },
    { id: 3, name: 'fuckthisshit' }
  ];
</script>

<ul>
  {#each workspaces as workspace}
    <li>
      <a href="/{$currentUser?.username}/workspace/{workspace.id}">{workspace.name}</a>
      <form method="POST" action="?/deleteWorkspace" use:enhance>
        <input hidden name="workspaceId" value={workspace.id} />
        <button>DELETE</button>
      </form>
    </li>
  {/each}

  <form method="POST" action="?/createWorkspace" use:enhance>
    <input
      name="workspaceName"
      type="text"
      size="30"
      maxlength="30"
      placeholder="NEW WORKSPACE NAME"
      required
    />
    <button>CREATE NEW</button>
  </form>
</ul>

<style lang="scss">
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
      justify-content: space-between;
      align-items: stretch;
      gap: 1em;
      margin-top: 1em;

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
