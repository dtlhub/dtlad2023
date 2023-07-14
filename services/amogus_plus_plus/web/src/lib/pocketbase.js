import PocketBase from 'pocketbase';
import { writable } from 'svelte/store';

export const pocketbase = new PocketBase('http://localhost:1984').autoCancellation(false);

export const currentUser = writable(pocketbase.authStore.model);
