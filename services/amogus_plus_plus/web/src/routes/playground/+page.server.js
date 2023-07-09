import { mustBeLoggedIn } from '$lib/auth/guards.js';

export async function load({ locals }) {
  mustBeLoggedIn(locals);
}

export const actions = {
  createWorkspace: async ({ locals, request }) => {},
  deleteWorkspace: async ({ locals, request }) => {}
};
