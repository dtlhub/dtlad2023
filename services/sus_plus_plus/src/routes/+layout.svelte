<script>
	import '../reset.css';

	/**
	 * @type {HTMLAudioElement}
	 */
	let audio;

	function startAudio() {
		audio.play();
	}
</script>

<audio bind:this={audio} src="/audio/theme.mp3" loop />

<svelte:window on:click={startAudio} />

<main>
	<slot />
</main>

<style>
	:global(body) {
		width: 100vw;
		height: 100vh;

		background-image: url('/images/stars.png');
		background-repeat: no-repeat;
		background-size: cover;

		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
