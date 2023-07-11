import { mustBeLoggedIn, mustOwnWorkspace } from '$lib/auth/guards';
import { fileContents, saveFile } from '$lib/server/workspaceUtils';
import { error, json } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function GET({ locals, params }) {
  mustBeLoggedIn(locals);
  await mustOwnWorkspace(locals, params);

  try {
    const fileData = fileContents(params.workspaceId, params.filename);
    return json(fileData.toString());
  } catch {
    throw error(400, 'Unable to read file');
  }
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ locals, params, request }) {
  mustBeLoggedIn(locals);
  await mustOwnWorkspace(locals, params);

  /** @type {{filename: string, content: string}} */
  const data = await request.json();

  try {
    saveFile(params.workspaceId, data.filename, data.content);
  } catch {
    throw error(500, 'Unable to save file');
  }

  return json({ ok: true });
}
