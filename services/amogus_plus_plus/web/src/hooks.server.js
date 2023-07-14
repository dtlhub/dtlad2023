import { pocketbase } from '$lib/server/pocketbase';

export const handle = async ({ event, resolve }) => {
  pocketbase.authStore.loadFromCookie(event.request.headers.get('cookie') || '');
  if (pocketbase.authStore.isValid) {
    try {
      await pocketbase.collection('users').authRefresh();
    } catch (err) {
      pocketbase.authStore.clear();
    }
  }
  const user = pocketbase.authStore.model;

  event.locals.pocketbase = pocketbase;
  if (user) {
    event.locals.user = user;
  }

  const response = await resolve(event);

  response.headers.set('set-cookie', pocketbase.authStore.exportToCookie({ httpOnly: false }));

  return response;
};
