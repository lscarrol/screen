<script>
  let username = '';
  let password = '';
  let twoFactorCode = '';
  let requires2FA = false;
  let error = '';

  async function login() {
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (data.requires2FA) {
        requires2FA = true;
        // You can display the list of trusted devices to the user if needed
        console.log(data.devices);
      } else {
        // Login successful, trigger the scheduled function
        triggerScheduledFunction();
      }
    } catch (err) {
      error = 'An error occurred during login.';
      console.error(err);
    }
  }

  async function submitTwoFactorCode() {
    try {
      const response = await fetch('/validate-2fa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, twoFactorCode }),
      });

      if (response.ok) {
        // 2FA validation successful, trigger the scheduled function
        triggerScheduledFunction();

        // Print the response data
        const data = await response.json();
        console.log('2FA Validation Response:', data);
      } else {
        error = 'Invalid 2FA code. Please try again.';

        // Print the error response
        const errorData = await response.json();
        console.log('2FA Validation Error:', errorData);
      }
    } catch (err) {
      error = 'An error occurred during 2FA validation.';
      console.error('2FA Validation Error:', err);
    }
  }

  async function triggerScheduledFunction() {
    try {
      const response = await fetch('/trigger-scheduled-function', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),  // Add this line to send the password in the request payload
      });

      if (response.ok) {
        console.log('Scheduled function triggered successfully');
      } else {
        console.error('Failed to trigger scheduled function');
      }
    } catch (err) {
      console.error('Error triggering scheduled function:', err);
    }
  }
</script>

<div>
  <h2>Login</h2>
  {#if !requires2FA}
    <form on:submit|preventDefault={login}>
      <input type="text" bind:value={username} placeholder="Username" required />
      <input type="password" bind:value={password} placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  {:else}
    <form on:submit|preventDefault={submitTwoFactorCode}>
      <input type="text" bind:value={twoFactorCode} placeholder="2FA Code" required />
      <button type="submit">Submit</button>
    </form>
  {/if}
  {#if error}
    <p>{error}</p>
  {/if}
</div>