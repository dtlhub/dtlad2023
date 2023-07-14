import { mustBeLoggedIn, mustOwnWorkspace } from '$lib/auth/guards.js';
import { error } from '@sveltejs/kit';
import { addFile, workspaceFiles, removeFile } from '$lib/server/workspaceUtils';

export async function load({ locals, params }) {
  mustBeLoggedIn(locals);
  const workspace = await mustOwnWorkspace(locals, params);

  return {
    id: workspace.id,
    name: workspace.name,
    files: workspaceFiles(params.workspaceId)
  };
}

export const actions = {
  createFile: async ({ locals, request, params }) => {
    mustBeLoggedIn(locals);
    await mustOwnWorkspace(locals, params);

    /** @type {{filename: string}} */
    // @ts-ignore
    const data = Object.fromEntries(await request.formData());

    try {
      addFile(params.workspaceId, data.filename);
    } catch {
      throw error(500, 'Unable to create file');
    }

    return workspaceFiles(params.workspaceId);
  },

  deleteFile: async ({ locals, request, params }) => {
    mustBeLoggedIn(locals);
    await mustOwnWorkspace(locals, params);

    /** @type {{filename: string}} */
    // @ts-ignore
    const data = Object.fromEntries(await request.formData());

    try {
      removeFile(params.workspaceId, data.filename);
    } catch {
      throw error(500, 'Unable to create file');
    }

    return workspaceFiles(params.workspaceId);
  }
};
