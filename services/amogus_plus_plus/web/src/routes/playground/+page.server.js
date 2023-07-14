import { mustBeLoggedIn } from '$lib/auth/guards.js';
import { tryHandlePocketbaseError } from '$lib/server/pocketbase.js';
import { deleteWorkspace } from '$lib/server/workspaceUtils.js';
import { error, redirect } from '@sveltejs/kit';

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
    workspaces: workspaces.map((pbWorkspace) => {
      return {
        id: pbWorkspace.id,
        name: pbWorkspace.name,
        description: pbWorkspace.description
      };
    })
  };
}

export const actions = {
  createWorkspace: async ({ locals, request }) => {
    mustBeLoggedIn(locals);

    /** @type {{name: string, description: string | null}} */
    // @ts-ignore
    const data = Object.fromEntries(await request.formData());

    let workspace = null;
    try {
      workspace = await locals.pocketbase.collection('workspaces').create({
        name: data.name,
        owner: locals.user?.id,
        description: data.description
      });
    } catch (err) {
      tryHandlePocketbaseError(err);
    }

    throw redirect(302, `/workspace/${workspace?.id}`);
  },

  deleteWorkspace: async ({ locals, request }) => {
    mustBeLoggedIn(locals);

    /** @type {{id: string}} */
    // @ts-ignore
    const data = Object.fromEntries(await request.formData());

    try {
      await locals.pocketbase.collection('workspaces').delete(data.id);
    } catch (err) {
      tryHandlePocketbaseError(err);
    }

    try {
      deleteWorkspace(data.id);
    } catch (err) {
      throw error(500, 'Unable to delete workspace');
    }

    throw redirect(302, '/playground');
  }
};
