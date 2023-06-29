import { tryHandlePocketbaseError } from '$lib/server/pocketbase.js';
import { redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ locals, request }) => {
		/** @type {{username: string, email: string, password: string, passwordConfirm: string}}   */
		// @ts-ignore
		const data = Object.fromEntries(await request.formData());

		data.passwordConfirm = data.password;

		try {
			await locals.pocketbase.collection('users').create(data);
			await locals.pocketbase.collection('users').authWithPassword(data.username, data.password);
		} catch (err) {
			tryHandlePocketbaseError(err);
		}

		throw redirect(303, '/');
	}
};
