<script>
	/** @type {string} */
	let value;

	function onChange() {
		console.log(value);
	}
</script>

<textarea bind:value on:input={onChange} on:change={onChange} on:paste={onChange} />

<style>
	textarea {
		padding: 0.2em 0.4em;

		background-color: var(--surface);

		border: 1px solid var(--white);
		border-radius: 1em;

		font-family: inherit;
		font-size: 1em;
		color: color-mix(in srgb, var(--white), var(--surface));
	}
</style>
