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

	<slot />
</main>

<style lang="scss">
	nav {
		$nav-height: 3em;
		height: $nav-height;
		display: flex;
		justify-content: space-between;
		align-items: center;
		background-color: rgba(0, 0, 0, 0.75);
		margin-bottom: -1 * $nav-height;
		
		ul {
			display: flex;
			justify-content: space-around;
			align-items: center;

			li a {
				margin: 0 0.6em;
				color: white;
				text-decoration: none;
			}
			.amogus {
				display: inline;
				font-size: 2em;
				color: #c51111;
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
	}
</style>
