<script>
	import '../reset.css';
	import FlyingAmogus from '$lib/FlyingAmogus.svelte';

	/**
	 * @type {HTMLAudioElement}
	 */
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
		<li><a href="/playground">Playground</a></li>
	</ul>
	<ul>
		<li><a href="/auth/login">Login</a></li>
		<li><a href="/auth/signup">Sign up</a></li>
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
		font-size: 1.5em;
	}

	nav {
		$nav-height: 3em;
		height: $nav-height;
		display: flex;
		justify-content: space-between;
		align-items: center;
		background-color: var(--surface);
		margin-bottom: -1 * $nav-height;

		ul {
			display: flex;
			justify-content: space-around;
			align-items: center;

			li a {
				padding: 0 0.6em;
				color: var(--white);
				text-decoration: none;

				&:hover {
					color: var(--cyan);
				}
			}
			.amogus {
				display: inline;
				font-size: 2em;
				color: var(--red);

				&:hover {
					color: var(--red);
				}
			}
		}
		position: relative;
	}

	main {
		width: 100vw;
		height: 100vh;

		background-image: url('/images/stars.png');
		background-repeat: no-repeat;
		background-size: cover;

		display: flex;
		justify-content: center;
		align-items: center;

		position: relative;
		z-index: -2;

		section {
			background-color: var(--surface);
			padding: 2em;
			max-width: 80%;
			border-radius: 1em;
		}
	}
</style>
