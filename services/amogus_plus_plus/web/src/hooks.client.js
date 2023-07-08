import { currentUser, pocketbase } from '$lib/pocketbase';

pocketbase.authStore.loadFromCookie(document.cookie);
pocketbase.authStore.onChange(() => {
  currentUser.set(pocketbase.authStore.model);
  document.cookie = pocketbase.authStore.exportToCookie({ httpOnly: false });
});
