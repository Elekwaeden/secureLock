// SecureLock PWA App Registration and Initialization

// Register Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then((registration) => {
        console.log('SecureLock: Service Worker registered successfully', registration);
        
        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'activated') {
              console.log('SecureLock: New service worker activated');
              showUpdateNotification();
            }
          });
        });
      })
      .catch((error) => {
        console.log('SecureLock: Service Worker registration failed:', error);
      });
  });
}

// PWA Install Prompt Handling
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (event) => {
  console.log('SecureLock: Install prompt ready');
  event.preventDefault();
  deferredPrompt = event;
  showInstallPrompt();
});

function showInstallPrompt() {
  // Create install button if it doesn't exist
  const installButton = document.getElementById('install-button');
  if (installButton) {
    installButton.style.display = 'inline-block';
    installButton.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`SecureLock: User response: ${outcome}`);
        deferredPrompt = null;
        installButton.style.display = 'none';
      } else {
        // fallback to showing instructions modal
        if (document.getElementById('installModal')) {
          const modal = new bootstrap.Modal(document.getElementById('installModal'));
          modal.show();
        } else {
          alert('To install SecureLock: open Chrome menu (⋮) → Install SecureLock');
        }
      }
    });
  }
}

// Handle app installation
window.addEventListener('appinstalled', () => {
  console.log('SecureLock: App installed successfully');
  deferredPrompt = null;
  // You can track installation metrics here
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/install-event', { timestamp: new Date().toISOString() });
  }
});

// Detect standalone mode (app installed)
if (window.navigator.standalone === true) {
  console.log('SecureLock: Running in standalone mode');
  document.body.classList.add('standalone-mode');
}

// Handle viewport for mobile app
window.addEventListener('resize', () => {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
});

// Initial viewport setup
const vh = window.innerHeight * 0.01;
document.documentElement.style.setProperty('--vh', `${vh}px`);

// Prevent user zoom on touch devices (security feature)
document.addEventListener('touchmove', (event) => {
  if (event.scale !== 1) {
    event.preventDefault();
  }
}, { passive: false });

// Network status indicator
function updateConnectionStatus() {
  const isOnline = navigator.onLine;
  const statusElement = document.getElementById('connection-status');
  
  if (statusElement) {
    if (isOnline) {
      statusElement.innerHTML = '<i class="bi bi-wifi"></i>';
      statusElement.classList.remove('offline');
    } else {
      statusElement.innerHTML = '<i class="bi bi-wifi-off"></i>';
      statusElement.classList.add('offline');
    }
  }
}

window.addEventListener('online', updateConnectionStatus);
window.addEventListener('offline', updateConnectionStatus);
document.addEventListener('DOMContentLoaded', updateConnectionStatus);

// Add install button functionality
function addInstallButton() {
  // Prefer a dedicated nav actions container, fallback to navbar-brand parent
  const navActions = document.getElementById('nav-actions');
  const navbar = document.querySelector('.navbar-brand');
  if ((navActions || navbar) && !document.getElementById('install-button')) {
    const installBtn = document.createElement('button');
    installBtn.id = 'install-button';
    installBtn.className = 'btn btn-sm btn-outline-info';
    installBtn.innerHTML = '<i class="bi bi-download"></i> Install';
    installBtn.style.display = 'none';
    if (navActions) {
      navActions.appendChild(installBtn);
    } else {
      navbar.parentElement.insertAdjacentElement('beforeend', installBtn);
    }
    // ensure visible inline-block so it fits navbar layout when shown
    installBtn.style.display = 'none';
    // Create a fallback help/install instructions button
    if (!document.getElementById('install-help')) {
      const helpBtn = document.createElement('button');
      helpBtn.id = 'install-help';
      helpBtn.className = 'btn btn-sm btn-outline-info ms-2';
      helpBtn.innerHTML = '<i class="bi bi-info-circle"></i>';
      helpBtn.title = 'Install instructions';
      helpBtn.style.display = 'none';
      if (navActions) {
        navActions.appendChild(helpBtn);
      } else {
        navbar.parentElement.insertAdjacentElement('beforeend', helpBtn);
      }
      helpBtn.addEventListener('click', () => {
        if (document.getElementById('installModal')) {
          const modal = new bootstrap.Modal(document.getElementById('installModal'));
          modal.show();
        } else {
          alert('To install SecureLock: open Chrome menu (⋮) → Install SecureLock');
        }
      });
    }
  }
}

document.addEventListener('DOMContentLoaded', addInstallButton);

// Share API support
if (navigator.share) {
  console.log('SecureLock: Web Share API supported');
}

// Notification permission
function requestNotificationPermission() {
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission().then((permission) => {
      console.log('SecureLock: Notification permission:', permission);
    });
  }
}

// Update notification
function showUpdateNotification() {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification('SecureLock Update', {
      body: 'A new version is available!',
      icon: '/static/icons/icon-192x192.png',
      tag: 'securelock-update',
    });
  } else {
    const alert = document.createElement('div');
    alert.className = 'alert alert-info alert-dismissible fade show';
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
      A new version of SecureLock is available!
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.prepend(alert);
  }
}

console.log('SecureLock: PWA App initialized');

// If the beforeinstallprompt event never fires, show a help button after a short delay
document.addEventListener('DOMContentLoaded', () => {
  // wait briefly for `beforeinstallprompt` to possibly fire
  setTimeout(() => {
    const installHelp = document.getElementById('install-help');
    const installBtn = document.getElementById('install-button');
    const isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
    if (isChrome && !deferredPrompt) {
      if (installHelp) installHelp.style.display = 'inline-block';
      if (installBtn) installBtn.style.display = 'none';
    }
  }, 1500);
});
