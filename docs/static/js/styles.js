/*
 * The first viewport is covered by critical.css. Apply the full editorial
 * system on user intent, or shortly after load when the browser is idle.
 */
const fullStyles = document.querySelector('#full-styles');

if (fullStyles) {
  let activated = false;
  const activate = () => {
    if (activated) return;
    activated = true;
    fullStyles.media = 'all';
  };

  ['pointerdown', 'keydown', 'wheel', 'touchstart'].forEach((eventName) => {
    addEventListener(eventName, activate, { once: true, passive: true });
  });

  addEventListener(
    'load',
    () => {
      setTimeout(activate, 3500);
    },
    { once: true },
  );
}
