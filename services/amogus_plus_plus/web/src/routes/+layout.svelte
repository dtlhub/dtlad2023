<script>
	import '../reset.css';
	import FlyingAmogus from '$lib/FlyingAmogus.svelte';
	import { currentUser, pocketbase } from '$lib/pocketbase';
	import { applyAction, enhance } from '$app/forms';

	/** @type {HTMLAudioElement} */
	let audio;

	function startAudio() {
		audio.play();
	}
</script>

<svelte:head>
	<title>ඞ++</title>
</svelte:head>

<audio bind:this={audio} src="/audio/theme.mp3" loop />

<svelte:window on:click={startAudio} />

<nav>
	<ul>
		<li><a href="/" class="amogus">ඞ++</a></li>
		<li><a href="/docs">Docs</a></li>
		{#if $currentUser}
			<li><a href="/playground">Playground</a></li>
		{/if}
	</ul>
	<ul>
		{#if $currentUser}
			<li>
				<span class="text">Logged in as <span class="username">{$currentUser.username}</span></span>
			</li>
			<li>
				<form
					method="POST"
					action="/auth/logout"
					use:enhance={() => {
						return async ({ result }) => {
							pocketbase.authStore.clear();
							await applyAction(result);
						};
					}}
				>
					<button type="submit">Log out</button>
				</form>
			</li>
		{:else}
			<li><a href="/auth/login">Log in</a></li>
			<li><a href="/auth/signup">Sign up</a></li>
		{/if}
	</ul>
</nav>

<main>
	{#each { length: 100 } as _}
		<FlyingAmogus />
	{/each}

	<section>
		<slot />
	</section>
</main>

<style lang="scss">
	@font-face {
		font-family: 'AmaticSC';
		font-style: normal;
		font-weight: 400;
		src: url('/fonts/AmaticSC-Bold.ttf');
	}
	:global(body) {
		--white: #d6e0f0;
		--red: #c51111;
		--blue: #132ed1;
		--pink: #ed54ba;
		--orange: #ef7d0d;
		--yellow: #f5f557;
		--purple: #6b2fbb;
		--cyan: #38fedc;
		--lime: #50ef39;
		--brown: #71491e;
		--surface: rgba(0, 0, 0, 0.75);

		font-family: AmaticSC;
		font-size: 2em;
	}

	$nav-height: 3em;
	nav {
		width: 100%;
		height: $nav-height;
		display: flex;
		justify-content: space-between;
		align-items: center;
		background-color: var(--surface);
		margin-bottom: -1 * $nav-height;
		z-index: 1;

		ul {
			display: flex;
			justify-content: space-around;
			align-items: center;

			li {
				.text,
				button,
				a {
					background: none;
					outline: none;
					border: none;
					font-family: inherit;
					font-size: inherit;
					padding: 0 0.6em;
					color: var(--white);
					text-decoration: none;
				}

				.text .username {
					color: var(--cyan);
				}

				button,
				a {
					&:hover {
						cursor: pointer;
						color: var(--cyan);
					}
				}
			}
			.amogus {
				display: inline;
				font-size: 2em;
				padding: 0 0.3em;
				color: var(--red);

				&:hover {
					color: var(--red);
				}
			}
		}
		position: relative;
	}

	main {
		width: 100%;
		min-height: 100vh;

		background-image: url('/images/stars.png');
		background-repeat: no-repeat;
		background-size: cover;
		background-attachment: fixed;

		display: flex;
		justify-content: center;
		align-items: center;

		position: relative;
		z-index: 0;

		section {
			background-color: var(--surface);
			padding: 2em;
			margin-top: $nav-height + 1em;
			margin-bottom: 1em;
			max-width: 80%;
			border-radius: 1em;
			z-index: unset;
		}
	}
</style>
