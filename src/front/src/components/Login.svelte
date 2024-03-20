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
      body: JSON.stringify({ username, password, twoFactorCode }),  // Include the password in the request payload
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

<div class="min-h-screen flex items-center justify-center bg-gray-100">
  <div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full fade-in">
    <div class="flex justify-center mb-8">
      <svg viewBox="0 0 75 75" width="75" height="75">
        <g transform="matrix(1,0,0,1,0,0)">
          <circle cx="37.5" cy="37.5" r="37.5" fill="#f1f3f4"></circle>
          <path d="M42.086 28.197C43.357 26.724 44.28 24.76 44.28 22.745C44.28 22.611 44.268 22.478 44.244 22.366C43.181 22.406 41.921 23.076 41.116 23.957C40.506 24.58 39.898 25.605 39.898 26.669C39.898 26.822 39.921 26.974 39.938 27.012C39.999 27.026 40.1 27.04 40.204 27.04C41.173 27.04 42.354 26.362 43.151 25.627L43.151 25.626L42.086 28.197ZM42.858 30.054C41.278 30.054 39.954 31.098 38.606 31.098C37.196 31.098 35.654 30.117 33.895 30.117C30.969 30.117 28 32.596 28 37.105C28 39.494 28.986 42.025 30.185 43.672C31.168 45.027 32 46.109 33.254 46.109C34.497 46.109 35.115 45.258 37.061 45.258C39.025 45.258 39.524 46.075 40.867 46.075C42.164 46.075 43.181 44.941 44.054 43.749C45.034 42.371 45.394 41.004 45.405 40.958C45.339 40.936 42.459 39.679 42.459 36.348C42.459 33.48 44.405 32.221 44.577 32.103C43.155 30.166 41.044 30.054 40.257 30.054L42.858 30.054Z" fill="#1d1d1f"></path>
        </g>
      </svg>
    </div>
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-6">Sign in with Apple ID</h2>
    {#if !requires2FA}
      <form on:submit|preventDefault={login} class="space-y-4">
        <div>
          <input type="text" id="username" bind:value={username} placeholder="Apple ID" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" />
        </div>
        <div>
          <input type="password" id="password" bind:value={password} placeholder="Password" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" />
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-600 transition duration-300 ease-in-out">
          Sign In
        </button>
      </form>
    {:else}
      <form on:submit|preventDefault={submitTwoFactorCode} class="space-y-4">
        <div>
          <input type="text" id="twoFactorCode" bind:value={twoFactorCode} placeholder="Enter 2FA Code" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" />
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-600 transition duration-300 ease-in-out">
          Submit
        </button>
      </form>
    {/if}
    {#if error}
      <p class="text-red-500 mt-4">{error}</p>
    {/if}
  </div>
</div>