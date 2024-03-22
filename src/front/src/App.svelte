<script>
	import { onMount } from 'svelte';
	import Login from './components/Login.svelte';
	import CategorizedData from './components/CategorizedData.svelte';
	import './styles/tailwind.css';
  
	let loggedIn = false;
	let requires2FA = false;
	let error = '';
  
	onMount(async () => {
	  // Check if the user is already logged in
	  const response = await fetch('/check-login');
	  const data = await response.json();
	  if (data.loggedIn) {
		loggedIn = true;
	  }
	});
  
	function handleLogin() {
	  loggedIn = true;
	}
  </script>
  
  <main class="min-h-screen bg-gray-100">
	{#if !loggedIn}
	  <div class="fade-in">
		<Login on:login={handleLogin} bind:requires2FA bind:error />
	  </div>
	{:else}
	  <div class="fade-in">
		<CategorizedData />
	  </div>
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