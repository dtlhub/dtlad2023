import { LOCAL_POCKETBASE_ADDRESS } from '$env/static/private';
import { error } from '@sveltejs/kit';
import PocketBase from 'pocketbase';

export const pocketbase = new PocketBase(LOCAL_POCKETBASE_ADDRESS).autoCancellation(false);

/**
 * @param {any} err
 * @returns {never}
 */
export function tryHandlePocketbaseError(err) {
  let errorToThrow;
  try {
    /** @type {import('pocketbase').ClientResponseError} */
    const clientError = err;
    errorToThrow = error(clientError.status, clientError.message);
  } catch (notClientError) {
    console.error(notClientError);
    errorToThrow = notClientError;
  }

  throw errorToThrow;
}
