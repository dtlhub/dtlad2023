import { pocketbase } from '$lib/server/pocketbase';

export const handle = async ({ event, resolve }) => {
  pocketbase.authStore.loadFromCookie(event.request.headers.get('cookie') || '');
  if (pocketbase.authStore.isValid) {
    try {
      await pocketbase.collection('users').authRefresh();
    } catch {
      pocketbase.authStore.clear();
    }
  }

  event.locals.pocketbase = pocketbase;
  event.locals.user = structuredClone(pocketbase.authStore.model);

  const response = await resolve(event);

  response.headers.set('set-cookie', pocketbase.authStore.exportToCookie({ httpOnly: false }));

  return response;
};
