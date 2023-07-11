import { tryHandlePocketbaseError } from '$lib/server/pocketbase';
import { error } from '@sveltejs/kit';

/** @param {App.Locals} locals */
export function mustBeLoggedIn(locals) {
  if (!locals.user) throw error(403, 'You must be logged in to perform this action');
}

/**
 * @param {App.Locals} locals
 * @param {{workspaceId: string}} params
 */
export async function mustOwnWorkspace(locals, params) {
  let workspace = null;
  try {
    workspace = await locals.pocketbase.collection('workspaces').getOne(params.workspaceId);
  } catch (err) {
    console.log(err);
    tryHandlePocketbaseError(err);
  }

  if (workspace.owner !== locals.user?.id) {
    throw error(403, 'You must own workspace to view it');
  }

  return workspace;
}
