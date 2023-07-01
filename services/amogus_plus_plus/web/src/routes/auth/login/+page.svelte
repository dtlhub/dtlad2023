<script>
	import { applyAction, enhance } from '$app/forms';
	import { pocketbase } from '$lib/pocketbase';
</script>

<h1>Log in</h1>
<form
	method="POST"
	use:enhance={() => {
		return async ({ result }) => {
			pocketbase.authStore.loadFromCookie(document.cookie);
			await applyAction(result);
		};
	}}
>
	<section>
		<label for="username">Username</label>
		<input id="username" name="username" type="text" size="50" />
	</section>
	<section>
		<label for="password">Password</label>
		<input id="password" name="password" type="password" size="50" />
	</section>

	<button type="submit">Sign up</button>
</form>

<style lang="scss">
	h1 {
		color: var(--white);
		font-size: 2em;
		text-align: center;
		margin-bottom: 1em;
	}

	form {
		display: flex;
		flex-direction: column;

		section {
			display: flex;
			flex-direction: column;
			margin-top: 0.8em;

			label {
				color: var(--white);
				margin: 0 0 0.2em 0.1em;
			}

			input {
				background-color: transparent;
				outline: none;
				color: var(--white);
				border: 2px solid var(--white);
				padding: 0.4em;
				font-family: inherit;
				font-size: 0.8em;

				&:hover {
					border-color: var(--cyan);
				}

				&:focus {
					color: var(--cyan);
					border-color: var(--cyan);
				}
			}
		}

		button {
			font-size: inherit;
			font-family: inherit;
			margin-top: 1em;
			background-color: var(--cyan);
			outline: none;
			border: none;
			border-radius: 0.25em;

			&:hover {
				opacity: 0.8;
				cursor: pointer;
			}
		}
	}
</style>
