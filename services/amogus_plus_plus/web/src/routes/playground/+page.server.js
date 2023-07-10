import { mustBeLoggedIn } from '$lib/auth/guards.js';
import { tryHandlePocketbaseError } from '$lib/server/pocketbase.js';
import { redirect } from '@sveltejs/kit';

export async function load({ locals }) {
  mustBeLoggedIn(locals);

  // @ts-ignore
  let workspaces = [];
  try {
    workspaces = await locals.pocketbase.collection('workspaces').getFullList({
      sort: 'created'
    });
  } catch (err) {
    tryHandlePocketbaseError(err);
  }

  return {
    // @ts-ignore
    workspaces: workspaces.map((pbWorkspace) => {
      return { id: pbWorkspace.id, name: pbWorkspace.name };
    })
  };
}

export const actions = {
  createWorkspace: async ({ locals, request }) => {
    mustBeLoggedIn(locals);

    /** @type {{workspaceName: string}} */
    // @ts-ignore
    const data = Object.fromEntries(await request.formData());

    let workspace = null;
    try {
      workspace = await locals.pocketbase.collection('workspaces').create({
        name: data.workspaceName,
        owner: locals.user?.id
      });
    } catch (err) {
      tryHandlePocketbaseError(err);
    }

    throw redirect(302, `/workspace/${workspace?.id}`);
  },

  deleteWorkspace: async ({ locals, request }) => {
    mustBeLoggedIn(locals);

    /** @type {{workspaceId: string}} */
    // @ts-ignore
    const data = Object.fromEntries(await request.formData());

    try {
      await locals.pocketbase.collection('workspaces').delete(data.workspaceId);
    } catch (err) {
      tryHandlePocketbaseError(err);
    }

    throw redirect(302, '/playground');
  }
};
