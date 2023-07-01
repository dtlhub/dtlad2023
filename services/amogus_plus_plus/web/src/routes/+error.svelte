<script>
	import { page } from '$app/stores';
</script>

<h1>{$page.status}</h1>
<p>{$page.error?.message}</p>

<style>
	h1,
	p {
		text-align: center;
		color: var(--white);
	}

  h1 {
    font-size: 3em;
    margin-bottom: 1rem;
  }
</style>
