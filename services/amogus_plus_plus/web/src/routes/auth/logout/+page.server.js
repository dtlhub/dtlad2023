import { redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ locals }) => {
		locals.pocketbase.authStore.clear();
		locals.user = null;
		throw redirect(303, '/');
	}
};
