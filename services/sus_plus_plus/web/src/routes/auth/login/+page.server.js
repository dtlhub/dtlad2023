import { tryHandlePocketbaseError } from '$lib/server/pocketbase';
import { redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ locals, request }) => {
		/** @type {{username: string, password: string}} */
		// @ts-ignore
		const data = Object.fromEntries(await request.formData());

		try {
			await locals.pocketbase.collection('users').authWithPassword(data.username, data.password);
		} catch (err) {
			tryHandlePocketbaseError(err);
		}

		throw redirect(303, '/');
	}
};
