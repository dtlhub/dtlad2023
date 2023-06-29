import PocketBase from 'pocketbase';
import { writable } from 'svelte/store';

// TODO: Change this and add NGINX
export const pocketbase = new PocketBase('http://localhost:8090');

export const currentUser = writable(pocketbase.authStore.model);
