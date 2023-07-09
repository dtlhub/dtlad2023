import { error } from '@sveltejs/kit';

/** @param {App.Locals} locals */
export function mustBeLoggedIn(locals) {
  if (!locals.user) throw error(403, 'You must be logged in to view this page');
}
