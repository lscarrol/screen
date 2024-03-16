<script>
    let username = '';
    let password = '';
    let twoFactorCode = '';
    let requires2FA = false;
    let error = '';
    
    async function login() {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        });
    
        const data = await response.json();
        if (data.requires2FA) {
          requires2FA = true;
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
        const response = await fetch('/api/validate-2fa', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, twoFactorCode }),
        });
    
        if (response.ok) {
          // 2FA validation successful, trigger the scheduled function
          triggerScheduledFunction();
        } else {
          error = 'Invalid 2FA code. Please try again.';
        }
      } catch (err) {
        error = 'An error occurred during 2FA validation.';
        console.error(err);
      }
    }
    
    async function triggerScheduledFunction() {
      try {
        const response = await fetch('/api/trigger-scheduled-function', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username }),
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