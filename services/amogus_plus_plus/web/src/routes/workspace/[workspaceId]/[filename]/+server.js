import { mustBeLoggedIn, mustOwnWorkspace } from '$lib/auth/guards';
import { execute } from '$lib/server/amogus_plus_plus/execute';
import { fileContents, saveFile, workspaceFiles } from '$lib/server/workspaceUtils';
import { error, json } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function PUT({ locals, params, request }) {
  mustBeLoggedIn(locals);
  await mustOwnWorkspace(locals, params);

  /** @type {{content: string}} */
  const data = await request.json();

  try {
    saveFile(params.workspaceId, params.filename, data.content);
  } catch {
    throw error(500, 'Unable to save file');
  }

  return json({ ok: true });
}

/** @type {import('./$types').RequestHandler} */
export async function GET({ locals, params }) {
  mustBeLoggedIn(locals);
  await mustOwnWorkspace(locals, params);

  try {
    const fileData = fileContents(params.workspaceId, params.filename);
    return json(fileData.toString());
  } catch {
    throw error(500, 'Unable to read file');
  }
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ locals, params, request }) {
  mustBeLoggedIn(locals);
  await mustOwnWorkspace(locals, params);

  /** @type {{stdin: string}} */
  const { stdin } = await request.json();

  /** @type {{files: string[], stdout: string, errorMsg: string}} */
  let response = {
    files: [],
    stdout: '',
    errorMsg: ''
  };

  if (!params.filename.endsWith('.sus')) {
    response.errorMsg =
      'AMONGUSISABIGSUSSYBAKAHAHAHAHAHATHISLANGUAGEISREALLYCOOLPLEASEUSEITMYLIFEDEPENDSONITORELSEPLSPLSPLSPLSPLSPLSPLSkahyghdfhm++ script files must end with ".sus"';
  } else {
    try {
      const code = fileContents(params.workspaceId, params.filename).toString();
      response.stdout = execute(code, stdin, params.workspaceId);
    } catch (err) {
      if (err instanceof Error) {
        response.errorMsg = err.toString();
      } else {
        response.errorMsg = 'Unknown error occured while executing script';
      }
    }
  }

  try {
    response.files = workspaceFiles(params.workspaceId);
  } catch {
    response.errorMsg = 'Unable to list workspace files after script execution';
  }

  return json(response);
}
