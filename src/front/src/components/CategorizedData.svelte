<script>
  import { onMount } from 'svelte';
  
  let categorizedData = [];
  
  onMount(async () => {
    try {
      const response = await fetch('/categorized-data');
      categorizedData = await response.json();
    } catch (error) {
      console.error('Error fetching categorized data:', error);
    }
  });
</script>

<h1>Categorized Data</h1>
{#if categorizedData.length === 0}
  <p>No categorized data available.</p>
{:else}
  <ul>
    {#each categorizedData as item}
      <li>
        <strong>Category:</strong> {item.category}<br />
        <strong>Name:</strong> {item.name}<br />
        {#if item.location}
          <strong>Location:</strong> {item.location}<br />
        {/if}
        <strong>Description:</strong> {item.description}
      </li>
    {/each}
  </ul>
{/if}