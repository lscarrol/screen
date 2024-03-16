<script>
	import { onMount } from 'svelte';
	import Login from './components/Login.svelte';
	import CategorizedData from './components/CategorizedData.svelte';
	import './styles/tailwind.css';
	
	let loggedIn = false;
	
	function handleLogin() {
	  loggedIn = true;
	}
	</script>
	
	<main>
	  {#if !loggedIn}
		<Login on:login={handleLogin} />
	  {:else}
		<CategorizedData />
	  {/if}
	</main>
	
	<style>
	main {
	  text-align: center;
	  padding: 1em;
	  max-width: 240px;
	  margin: 0 auto;
	}
	
	@media (min-width: 640px) {
	  main {
		max-width: none;
	  }
	}
	</style>